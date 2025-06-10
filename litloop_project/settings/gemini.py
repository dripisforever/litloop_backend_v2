 # https://gemini.google.com/app/266e12eb742bf3b4?hl=en
import os
import boto3

from litloop_project.settings.base import *

# Only if not DEBUG
if not os.getenv('DEBUG', 'False') == 'True':
    ssm_client = boto3.client('ssm', region_name='your-aws-region') # Or boto3.client('secretsmanager')

    def get_secret(param_name):
        try:
            response = ssm_client.get_parameter(
                Name=f'/django/prod/{param_name}', # Or your secret manager path
                WithDecryption=True
            )
            return response['Parameter']['Value']
        except Exception as e:
            print(f"Error fetching secret {param_name}: {e}")
            # Handle error appropriately, maybe raise an exception or provide a default
            return None

    POSTGRES_DB = get_secret("db_name")
    POSTGRES_USER = get_secret("db_user")
    POSTGRES_PASSWORD = get_secret("db_password")
    SECRET_KEY = get_secret("django_secret_key")


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

    # Add other settings from env or SSM
    # ALLOWED_HOSTS = [os.getenv('ALLOWED_HOST_1'), os.getenv('ALLOWED_HOST_2')]
else:
    # Development settings, maybe read from .env locally
    from dotenv import load_dotenv
    load_dotenv()
    POSTGRES_DB = os.getenv("DB_NAME")
    # ... etc for development
