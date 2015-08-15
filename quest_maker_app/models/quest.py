from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .quest_template import QuestTemplate

from django.utils import timezone
from datetime import datetime, timedelta


class Quest(models.Model):
    """A quest"""
    leader = models.ForeignKey(User, related_name="quests_led")
    users = models.ManyToManyField(User, through="UserQuest",
                                   through_fields=("quest", "user"))
    name = models.CharField(max_length=100, db_index=True)
    template = models.ForeignKey(QuestTemplate)
    start_date = models.DateField(default=timezone.now)
    users_last_updated = models.DateTimeField()
    hours_offset_utc = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property 
    def waypoint_set(self):
        return self.template.waypoint_set

    @property
    def last_waypoint(self):
        return self.template.last_waypoint

    @property
    def length(self):
        return self.template.length

    @property
    def latest_day(self):
        if not hasattr(self, "_latest_day"):
            self._latest_day = self._get_latest_day()
        return self._latest_day
    
    def update_from_fitbit(self):
        """Update with various info from the fitbit API"""
        self.update_timezone_fitbit()
        self.update_dist_fitbit()
        self.update_total_miles()

    def update_dist_fitbit(self):
        """
        Update the db with the latest data from Fitbit for all the users in the 
        Quest
        """
        latest_info = {}
        for user_quest in self.user_quests.all():
            user = user_quest.user
            new_info = user.profile.update_dist_fitbit(
                begin_date=self.start_date, end_date=self.latest_day)
            latest_info[user.username] = new_info
        self.users_last_updated = timezone.now()
        self.save()
        return latest_info

    def update_timezone_fitbit(self):
        """
        Get the timezones from all fitbit users; set the quest timezone
        to be the latest one
        """
        utc_offsets = set()
        for user_quest in self.user_quests.all():
            user = user_quest.user
            utc_offsets.add(user.profile.get_timezone_fitbit())
        utc_offsets = utc_offsets - set([None])
        if len(utc_offsets) > 0:
            self.hours_offset_utc = min(utc_offsets)
            self.save()
            return self.hours_offset_utc

    def update_total_miles(self):
        for user_quest in self.user_quests.all():
            user_quest.update_total_miles()

    def get_users_info(self):
        """Get a dict of info about all users on the quest
        """
        info = {}
        for user_quest in self.user_quests.all():
            user = user_quest.user
            info[user.username] = user_quest.get_info()
        return info

    def _get_latest_day(self):
        """
        Get the latest data we will report to the user.  We want to report 
        yesterday's data, where "yesterday" is defined according to the timezone
        of the quest.
        """
        return (timezone.now() 
                + timedelta(hours=self.hours_offset_utc)
                - timedelta(days=1)
                ).date()

    def __unicode__(self):
        return "Quest id={} name={}".format(self.pk, self.name)
