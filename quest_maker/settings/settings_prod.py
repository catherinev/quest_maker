import os
import dj_database_url
from quest_maker.settings.settings_base import *


try:
    SECRET_KEY = os.environ['QUEST_MAKER_SECRET_KEY']

    # encryption for prod
    ENCRYPTION_KEY = os.environ["ENCRYPTION_KEY"]
    INIT_VECTOR = os.environ["INIT_VECTOR"]
except KeyError:
    # this may happen when running migrations (etc) in prod
    pass

DEBUG = False
TEMPLATE_DEBUG = False

# Apps used specifically for production
INSTALLED_APPS += (
    'gunicorn',
)

# These people will get error emails in production
ADMINS = (
    ('Catherine', 'cvong47@gmail.com'),
)

# Set this to match the domains of the production site.
ALLOWED_HOSTS = [
    "catherinev.pythonanywhere.com"
]


