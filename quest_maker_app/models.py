from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

NOTABILITY_CHOICES = (
    ("high", "high"),
    ("medium", "medium"),
    ("low", "low")
    )

# Create your models here.
class QuestTemplate(models.Model):
    author = models.ForeignKey(User, related_name="quest_templates_created")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return "QuestTemplate {}, id={}".format(self.name, self.pk)

class Quest(models.Model):
    """A quest.
    """

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
                "waypoint": user_quest.get_waypoint()
            }
        return info


    def __unicode__(self):
        return "Quest {}, id={}".format(self.name, self.pk)


class Waypoint(models.Model):
    """A waypoint on the quest
    """

    quest_template = models.ForeignKey(QuestTemplate)
    name = models.CharField(max_length=100)
    distance_from_start = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notability = models.CharField(choices=NOTABILITY_CHOICES, max_length=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __unicode__(self):
        return "Waypoint {}, id={}".format(self.name, self.pk)

class UserQuest(models.Model):
    user = models.ForeignKey(User)
    quest = models.ForeignKey(Quest, related_name="user_quests")
    character = models.CharField(max_length=100)
    total_miles = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def update_total_miles(self):
        pass

    def get_waypoint(self):
        pass

    def get_info(self):
        return {}

class DailyDistance(models.Model):
    # allows us to cache old data
    user = models.ForeignKey(User)
    miles = models.FloatField(null=True, blank=True)
    day = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

