from quest_maker.settings.settings_base import *

# This file is NOT part of our repo. It contains sensitive settings like secret key
# and db setup.
from env import *


DEBUG = True
TEMPLATE_DEBUG = True

# Apps used specifically for development
INSTALLED_APPS += (

)




#For development, I don't actually send emails.
# This makes emails print to the console:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Alternatively, if I wanted them to print to a text file, create
# this folder:
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/emails_testing'


# Development hosts: localhost i.e. 127.0.0.1
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
