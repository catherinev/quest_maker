from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class QuestTemplate(models.Model):
    """A template for a quest.  Can be used as a template for many quests."""
    author = models.ForeignKey(User, related_name="quest_templates_created")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ## TO DO: add validation that checks for a waypoint
    ## with distance 0; add a default if missing
    @property
    def last_waypoint(self):
        sorted_waypoints = sorted(
            self.waypoint_set.all(), key=lambda x: x.distance_from_start)
        return sorted_waypoints[-1]

    @property
    def length(self):
        return self.last_waypoint.distance_from_start

    @property
    def ordered_waypoint_list(self):
        try:
            return self._ordered_waypoint_list
        except AttributeError:
            self._ordered_waypoint_list = list(
                self.waypoint_set.order_by('distance_from_start'))
            return self._ordered_waypoint_list
    
    def __unicode__(self):
        return "QuestTemplate id={} name={}".format(self.pk, self.name)
