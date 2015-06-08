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
)

LOCAL_APPS = (
    'quest_maker_app',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# This enables us to access request data from a template, for example
# so we can access the current page's url.
# See here: http://stackoverflow.com/questions/7665514/django-highlight-navigation-based-on-current-page
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
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
