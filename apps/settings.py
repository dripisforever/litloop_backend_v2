# reference: https://stackoverflow.com/questions/3948356/how-to-keep-all-my-django-applications-in-specific-folder
import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

INSTALLED_APPS = [

     'apps.users.apps.UsersConfig',
     '',

]
