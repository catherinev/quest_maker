from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .quest import Quest
from .daily_distance import DailyDistance
from .. import util

class UserQuest(models.Model):
    """
    Join table between user and quest.  Represents a user on a particular quest
    """
    user = models.ForeignKey(User)
    quest = models.ForeignKey(Quest, related_name="user_quests")
    character = models.CharField(max_length=100)
    total_miles = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "quest")

    @property
    def daily_distances(self):
        if not hasattr(self, "_daily_distances"):
            self._daily_distances = self.user.dailydistance_set.filter(
                day__gte=self.quest.start_date)
        return self._daily_distances

    @property
    def latest_day(self):
        if not hasattr(self, "_latest_day"):
            self._latest_day = self.quest.latest_day
        return self._latest_day

    @property 
    def day_finished(self):
        if not hasattr(self, "_day_finished"):
            self._day_finished = self._get_day_finished()
        return self._day_finished

    def _get_day_finished(self):
        """Determine the day the user has finished the quest"""
        length = self.quest.length
        if self.total_miles < length:
            return None
        else:
            total = 0
            daily_distances = sorted(self.daily_distances, key=lambda x: x.day)
            for daily_distance in daily_distances:
                total += daily_distance.miles
                if total >= length:
                    return daily_distance.day
    
    def update_total_miles(self):
        self.total_miles = self.get_total_miles()
        self.save()
        return self.total_miles

    def get_total_miles(self, start_date=None, end_date=None):
        """
        Alias for the get_total_miles method on Profile, where the
        start_date is set to default to the start_date of the quest.
        """
        if start_date is None:
            start_date = self.quest.start_date
        return self.user.profile.get_total_miles(start_date=start_date, 
                                                 end_date=end_date)

    def get_waypoint(self, day=None):
        """Find the last waypoint passed as of the given day"""
        if day is None:
            day = self.latest_day
        distance_traveled = self.get_total_miles(end_date=day)
        
        waypoints = self.quest.waypoint_set.all()
        waypoints = sorted(waypoints, key=lambda x: x.distance_from_start)
        
        passed_waypoints = filter(
            lambda x: x.distance_from_start <= distance_traveled,
            waypoints)
        return passed_waypoints[-1]

    def get_info(self):
        """Get summary of latest info for the user"""
        return {
            "name": self.user.username,
            "quest": self.quest.name,
            "character": self.character,
            "total_miles": self.get_total_miles(end_date=self.latest_day),
            "waypoint": self.get_waypoint(),
            "user_id": self.user.id,
            "day_finished": self.day_finished
        }

    def get_daily_info(self):
        """Get daily info for each day in the quest, reverse sorted by day"""
        start_date = self.quest.start_date
        last_day = self.day_finished or self.latest_day
        info = []
        # get daily info from the database
        for datum in self.user.dailydistance_set.filter(
            day__range=[start_date, last_day]):
            info.append({
                "day": datum.day,
                "daily_distance": datum.miles,
                "total_distance": self.get_total_miles(end_date=datum.day),
                "waypoint": self.get_waypoint(day=datum.day)
            })
        # add any days that aren't in the database
        days_in_db = {datum["day"] for datum in info}
        all_days_on_quest = set(
            util.daterange(start_date, last_day, inclusive=True))
        missing_days = all_days_on_quest - days_in_db
        for day in missing_days:
            info.append({
                "day": day,
                "daily_distance": "-",
                "total_distance": self.get_total_miles(end_date=day),
                "waypoint": self.get_waypoint(day=day)
            })

        info = sorted(info, key=lambda x: x["day"], reverse=True)
        return info
    
    def __unicode__(self):
        return "UserQuest id={} for user={} quest={}".format(self.pk, 
                                                             self.user_id, 
                                                             self.quest_id)

