from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Custom fields and methods for a user.  This is one-to-one with
    Django's built in User model.  Django's User model has not been altered
    and will only be used for user authentication.
    """
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    @property
    def fitbit_enabled(self):
        return self.user.social_auth.exists()

    @property
    def short_name(self):
        return "{} {}.".format(self.first_name, self.last_name[0])

    def __unicode__(self):
        return "Profile id={} for user with id={} username={}".format(
                self.pk, self.user_id, self.user.username)

