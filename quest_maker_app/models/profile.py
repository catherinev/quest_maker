from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from .daily_distance import DailyDistance
from .. import util

import fitbit
import datetime

FITBIT_KEY = settings.SOCIAL_AUTH_FITBIT_KEY
FITBIT_SECRET = settings.SOCIAL_AUTH_FITBIT_SECRET
MILLIS_PER_HOUR = 3600000.0


class Profile(models.Model):
    """
    Custom fields and methods for a user.  This is one-to-one with
    Django's built in User model.  Django's User model has not been altered
    and will only be used for user authentication.
    """
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def fitbit_enabled(self):
        return self.user.social_auth.exists()

    @property
    def authd_client(self):
        if not hasattr(self, "_authd_client"):
            self._authd_client = self.get_authd_client()
        return self._authd_client

    @property
    def short_name(self):
        return "{} {}.".format(self.first_name, self.last_name[0])

    def get_authd_client(self):
        """Connect to the Fitbit API using the user's credentials"""
        if self.fitbit_enabled:
            user_tokens = self.user.social_auth.get().access_token
            user_key = user_tokens["oauth_token"]
            user_secret = user_tokens["oauth_token_secret"]
            # note that system="en_US" ensures that we receive data in US 
            # units as defined here: https://wiki.fitbit.com/display/API/API+Unit+System
            authd_client = fitbit.Fitbit(FITBIT_KEY, 
                                         FITBIT_SECRET, 
                                         resource_owner_key=user_key, 
                                         resource_owner_secret=user_secret,
                                         system="en_US")
            
            return authd_client
        else:
            return None

    def update_dist_fitbit(self, begin_date=None, end_date=None):
        """
        Get and save the distances the user traveled, in miles, from begin_date 
        to end_date, inclusive.  This method gets data from Fitbit but doesn't 
        overwrite data for days that already exists in the database.

        begin_date and end_date should be of type datetime.date
        """
        begin_date, end_date = util.validate_date_range(begin_date, end_date)
        if self.fitbit_enabled:
            # 1. Get all the data we already have in the database
            db_distances = self.get_dist_db(begin_date, end_date)
            db_days = {datum.day for datum in db_distances}

            # 2. Get data from Fitbit
            fitbit_distances = self.get_dist_fitbit(begin_date, end_date)
            fitbit_days = {datum.day for datum in fitbit_distances}

            # 3. Add NEW data from Fitbit to db
            missing_days = fitbit_days - db_days
            new_fitbit_distances = []
            old_fitbit_distances = []
            for datum in fitbit_distances:
                if datum.day in missing_days:
                    new_fitbit_distances.append(datum)
                else:
                    old_fitbit_distances.append(datum)

            for datum in new_fitbit_distances:
                datum.save()
            self._update_past_week(old_fitbit_distances)

            return new_fitbit_distances

    def _update_past_week(self, fitbit_distances):
        """We may grab incomplete data from Fitbit.  For example, if a tracker
        gets synced on Wednesday afternoon, we update our app on Wednesday
        night, and then the tracker syncs again on Thursday, we need to make
        sure we pick up all the steps recorded between the Wednesday afternoon
        sync and EOD Wednesday.

        Since fitbit trackers only keep data for a week, we should not need to 
        check back further than 1 week.
        """
        seven_days_ago = (datetime.datetime.today() - datetime.timedelta(days=8)
            ).date()
        past_week = sorted(
            (datum for datum in fitbit_distances if datum.day >= seven_days_ago), 
            key=lambda datum: datum.day,
            reverse=True
        )
        for datum in past_week:
            old_distance = DailyDistance.objects.get(day=datum.day)
            if old_distance.miles == datum.miles:
                # if the distance hasn't changed, then any previous distances
                # also haven't changed
                break
            old_distance.miles = datum.miles
            old_distance.save()

    def get_dist_fitbit(self, begin_date, end_date):
        """
        Get distances by hitting Fitbit API.  Note that the distances will be
        returned in miles.
        """
        begin_date, end_date = util.validate_date_range(begin_date, end_date)
        fitbit_distances = self.authd_client.time_series('activities/distance', 
                                                           base_date=begin_date,
                                                           end_date=end_date)
        fitbit_distances = [
            DailyDistance(user=self.user, 
                          miles=datum["value"], 
                          day=util.fitbit_datetime_to_date(datum["dateTime"]),
                          manually_entered=False)
            for datum in fitbit_distances['activities-distance']]
        return fitbit_distances

    def get_dist_db(self, begin_date, end_date):
        """Get distances that are already stored in the database"""
        begin_date, end_date = util.validate_date_range(begin_date, end_date)
        
        distances = self.user.dailydistance_set.filter(
            day__range=[begin_date, end_date])
        return distances

    def get_timezone_fitbit(self):
        """Get the timezone the user has set via fitbit"""
        if self.fitbit_enabled:
            fitbit_user_info = self.authd_client.user_profile_get()["user"]
            return fitbit_user_info["offsetFromUTCMillis"] / MILLIS_PER_HOUR

    def get_total_miles(self, start_date=None, end_date=None):
        """
        Get the total number of miles the user traveled between the 
        start_date and end_date, inclusive
        """
        start_date, end_date = util.validate_date_range(start_date, end_date)
        daily_distances = self.user.dailydistance_set.filter(
            day__range=[start_date, end_date])
        return sum(day.miles for day in daily_distances)

    def __unicode__(self):
        return "Profile id={} for user with id={} username={}".format(
                self.pk, self.user_id, self.user.username)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Profile.objects.get(user=self.user)
                self.pk = p.pk
                # the following line should not be necessary
                # but, for unknown reasons, it is
                self.created_at = datetime.datetime.now()
            except Profile.DoesNotExist:
                pass

        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
