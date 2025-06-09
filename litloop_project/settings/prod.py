
from litloop_project.settings.base import *
import os

POSTGRES_DB = os.getenv("DB_NAME")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
POSTGRES_USER = os.getenv("DB_USER")
POSTGRES_HOST = os.getenv("DB_HOST")
POSTGRES_PORT = os.getenv("DB_PORT")



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}
DEBUG = False
ALLOWED_HOSTS=['*','https://litloop.netlify.app']
