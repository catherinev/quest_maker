from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .quest_template import QuestTemplate

NOTABILITY_CHOICES = (
    ("high", "high"),
    ("medium", "medium"),
    ("low", "low")
    )


class Waypoint(models.Model):
    """A waypoint on a quest template"""
    quest_template = models.ForeignKey(QuestTemplate)
    name = models.CharField(max_length=100)
    distance_from_start = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notability = models.CharField(choices=NOTABILITY_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rank(self):
        """Number of waypoint compared to other waypoints on the quest"""
        return self.quest_template.ordered_waypoint_list.index(self) + 1

    def __unicode__(self):
        return "Waypoint id={} name={}".format(self.pk, self.name)
