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

    def __unicode__(self):
        return "QuestTemplate id={} name={}".format(self.pk, self.name)
