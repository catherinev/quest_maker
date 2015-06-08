from django.db import models
from django.contrib.auth.models import User

from quest_maker_app.util import encrypt, decrypt


class Profile(models.Model):
    """
    Custom fields and methods for a user.  This is one-to-one with
    Django's built in User model.  Django's User model has not been altered
    and will only be used for user authentication.
    """
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fitbit_enabled = models.BooleanField(default=False, editable=False)
    encrypted_fitbit_key = models.CharField(null=True, blank=True,
                                            max_length=1000, editable=False)
    encrypted_fitbit_secret = models.CharField(null=True, blank=True, 
                                               max_length=1000, editable=False)
    encrypted_fitbit_userid = models.CharField(null=True, blank=True, 
                                               max_length=1000, editable=False)

    @property
    def short_name(self):
        return "{} {}.".format(self.first_name, self.last_name[0])

    def save(self, *args, **kwargs):
        """
        We override the save method so the fitbit credentials will be
        encrypted
        """
        try:
            # if new fitbit credentials have been added, encrypt them
            unencrypted_key = self.unencrypted_fitbit_key
            unencrypted_secret = self.unencrypted_fitbit_secret
            unencrypted_userid = self.unencrypted_fitbit_userid

            self.encrypted_fitbit_key = encrypt(unencrypted_key)
            self.encrypted_fitbit_secret = encrypt(unencrypted_secret)
            self.encrypted_fitbit_userid = encrypt(unencrypted_userid)
        except AttributeError:
            pass

        return super(Profile, self).save(*args, **kwargs)

    def set_fitbit_credentials(self, key, secret, userid):
        """
        Set newly retrieved fitbit credentials.  This saves the unencrypted 
        key, secret, and userid as attributes, which will all be encrypted upon 
        saving to the database (see the save method).
        """
        self.unencrypted_fitbit_key = key
        self.unencrypted_fitbit_secret = secret
        self.unencrypted_fitbit_userid = userid

    def get_fitbit_credentials(self):
        """Retrieve and unencrypt fitbit credentials"""
        return {
            "key": decrypt(self.encrypted_fitbit_key),
            "secret": decrypt(self.encrypted_fitbit_secret),
            "userid": decrypt(self.encrypted_fitbit_userid)
        }

    def __unicode__(self):
        return "Profile id={} for user with id={} username={}".format(
                self.pk, self.user_id, self.user.username)

