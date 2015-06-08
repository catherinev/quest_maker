from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .quest_template import QuestTemplate


class Quest(models.Model):
    """A quest"""
    leader = models.ForeignKey(User, related_name="quests_led")
    users = models.ManyToManyField(User, through="UserQuest",
                                   through_fields=("quest", "user"))
    name = models.CharField(max_length=100, db_index=True)
    template = models.ForeignKey(QuestTemplate)
    start_date = models.DateField(default=timezone.now)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    @property 
    def waypoints(self):
        return self.template.waypoints

    def get_latest_user_info(self):
        """Get a dict of all users, their current distances, and the waypoints
        they are currently at
        """
        info = {}
        for user_quest in self.user_quests.all():
            user = user_quest.user
            info[user.username] = {
                "character": user_quest.character,
                "distance_from_start": user_quest.update_total_miles(),
                "waypoint": user_quest.get_waypoint(),
                "user_id": user.id
            }
        return info

    def __unicode__(self):
        return "Quest id={} name={}".format(self.pk, self.name)
