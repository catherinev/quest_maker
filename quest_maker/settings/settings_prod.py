import os
import dj_database_url
from quest_maker.settings.settings_base import *


try:
    # This file is not part of the repo and contains secrets like db info.
    from env import *
# There is no env.py file on Heroku.
# We load from environment variables instead.
except ImportError:
    SECRET_KEY = os.environ['QUEST_MAKER_SECRET_KEY']

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

# encryption for prod
ENCRYPTION_KEY = os.environment["ENCRYPTION_KEY"]
INIT_VECTOR = os.environment["INIT_VECTOR"]
