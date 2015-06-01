from django.db import models
from django.contrib.auth.models import User

NOTABILITY_CHOICES = (
    ("high", "high"), 
    ("medium", "medium"), 
    ("low", "low")
    )

# Create your models here.
class Quest(models.Model):
    """A quest.
    """

    creator = models.ForeignKey(User, related_name="quests_created")
    users = models.ManyToManyField(User, related_name="quests")
    name = models.CharField(max_length=100, db_index=True)
    
    def __unicode__(self):
        return "Quest {}, id={}".format(self.name, self.pk)


class Waypoint(models.Model):
    """A waypoint on the quest
    """

    quest = models.ForeignKey(Quest)
    name = models.CharField(max_length=100)
    distance_from_start = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notability = models.CharField(choices=NOTABILITY_CHOICES, max_length=10)
    
    def __unicode__(self):
        return "Waypoint {}, id={}".format(self.name, self.pk)
