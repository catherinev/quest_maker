from django.db import models
from django.contrib.auth.models import User


class DailyDistance(models.Model):
    """Data regarding distance walked/run for a given user on a given day."""
    user = models.ForeignKey(User)
    miles = models.FloatField(null=True, blank=True)
    day = models.DateField()
    manually_entered = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "day")

    def __unicode__(self):
        return "DailyDistance id={} on day={} with miles={} for user={}".format(
                self.pk, self.day, self.miles, self.user_id)

