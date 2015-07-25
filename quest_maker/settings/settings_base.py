"""
Django settings for painindex project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# __file__ gives the full filepath of settings_base.py.
# os.path.dirname(__file__) gives the parent directory.
# We can repeat this to get the parent of the parent of the parent,
# which for our directory structure is the root directory of the project
import os
from os.path import dirname
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


BASE_DIR = dirname(dirname(dirname(__file__)))
# print BASE_DIR # (full path of project_dir)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "<my secret key>" 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'social.apps.django_app.default',
)

LOCAL_APPS = (
    'quest_maker_app',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTHENTICATION_BACKENDS = (
    'social.backends.fitbit.FitbitOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

# AUTH_USER_MODEL = 'quest_maker_app.models.CustomUser'
SOCIAL_AUTH_LOGIN_URL = '/fitbit-login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# This enables us to access request data from a template, for example
# so we can access the current page's url.
# See here: http://stackoverflow.com/questions/7665514/django-highlight-navigation-based-on-current-page
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'quest_maker.urls'

WSGI_APPLICATION = 'quest_maker.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'quest_maker/static/collect')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'quest_maker/static/css'),
    os.path.join(BASE_DIR, 'quest_maker/static/js'),
    os.path.join(BASE_DIR, 'quest_maker/static/bootstrap'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'quest_maker/templates'),
)

DATABASES = {
  'default': {
     'ENGINE': 'django.db.backends.sqlite3',
     'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
 }
}

# encryption for dev
ENCRYPTION_KEY = 'This is a key123'
INIT_VECTOR = 'This is an IV456'

# social auth
SOCIAL_AUTH_FITBIT_LOGIN_URL = '/fitbit/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
try:
    SOCIAL_AUTH_FITBIT_KEY = os.environ["FITBIT_KEY"]
    SOCIAL_AUTH_FITBIT_SECRET = os.environ["FITBIT_SECRET"]
except KeyError:
    msg = "You must set the FITBIT_KEY and FITBIT_SERCRET environment variables"
    raise KeyError(msg)