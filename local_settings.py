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

RUNKEEPER_CLIENT_ID = "13d88654b7ee44ccb47815996cbdb6aa"
RUNKEEPER_CLIENT_SECRET = "7f4b64b9a05d41b783af39e635d63cb0"

FATSECRET_REST_API_ACCESS_KEY = "f5bdcb99867d46b6ae0e8f5bd5140866"
FATSECRET_REST_API_CONSUMER_KEY = FATSECRET_REST_API_ACCESS_KEY
FATSECRET_REST_API_SHARED_SECRET = "a781b6c7f9b44255a2acbb70b914fbe1"

FATSECRET_REQUEST_TOKEN_EXTRA_ARGUMENTS = {
    "oauth_consumer_key" : FATSECRET_REST_API_CONSUMER_KEY,
    "oauth_signature_method" : "HMAC-SHA1", 
    "oauth_version" : "1.0",
    "method" : "profile.get_auth",
    "format": "json"
}

WIKILIFE = {
    "HOST": "http://localhost:7080"
}