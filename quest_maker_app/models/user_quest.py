from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .quest import Quest

class UserQuest(models.Model):
    """
    Join table between user and quest.  Represents a user on a particular quest
    """
    user = models.ForeignKey(User)
    quest = models.ForeignKey(Quest, related_name="user_quests")
    character = models.CharField(max_length=100)
    total_miles = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def update_total_miles(self):
        pass

    def get_waypoint(self):
        return "foo"

    def get_info(self):
        return {
            "name": self.user.username,
            "quest": self.quest.name,
            "character": self.character,
            "total_miles": self.total_miles,
            "last_waypoint": self.get_waypoint()
        }

    def get_daily_info(self):
        # return a list of dicts, one for each day
        pass

    def __unicode__(self):
        return "UserQuest id={} for user={} quest={}".format(self.pk, 
                                                             self.user_id, 
                                                             self.quest_id)

