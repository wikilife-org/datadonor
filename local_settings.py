# Django settings for website project.
from settings import *  # @UnusedWildImport

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'datadonor',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

#LOCAL
GOOGLE_OAUTH2_CLIENT_ID= "998456856470.apps.googleusercontent.com"
GOOGLE_OAUTH2_CLIENT_SECRET = "VytSb36-qpExvhaB13S_PweI"