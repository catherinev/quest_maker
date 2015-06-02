import os
from .settings_base import BASE_DIR

DATABASES = {
  'default': {
     'ENGINE': 'django.db.backends.sqlite3',
     'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
 }
}