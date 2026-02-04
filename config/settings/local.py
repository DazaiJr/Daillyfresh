from .base import *

# Development mein Debug ON rahega
DEBUG = True

ALLOWED_HOSTS = ['*']

# Development Database (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}