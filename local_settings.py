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


FACEBOOK_APP_ID ="167345460113739"
FACEBOOK_API_SECRET ="56fe36cce6798c4655fdb55827551b36"

EVERNOTE_CONSUMER_KEY = 'joaco-quintas'
EVERNOTE_CONSUMER_SECRET = '2598d741657d00de'


WIKILIFE = {
    "HOST": "http://localhost:7080"
}