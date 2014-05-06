from django.utils import simplejson

from social_auth.backends import BaseOAuth2, ConsumerBasedOAuth, OAuthBackend, PhysicalBackend
from social_auth.exceptions import AuthCanceled
import requests


# Moves configuration
MOVES_SERVER = 'https://api.moves-app.com/oauth/v1'
MOVES_REQUEST_TOKEN_URL = '%s/authorize' % MOVES_SERVER
MOVES_ACCESS_TOKEN_URL = '%s/access_token' % MOVES_SERVER
MOVES_AUTHORIZATION_URL = '%s/authorize' % MOVES_SERVER



class MovesBackend(OAuthBackend, PhysicalBackend):
    """Moves OAuth authentication backend"""
    name = 'moves'
    EXTRA_DATA = [('user_id', 'user_id')]
    ID_KEY = "user_id"

    def get_user_details(self, response):
        """Return user details from Moves account"""

        user_id = response['user_id']
        return {'user_id':user_id}

    @classmethod
    def tokens(cls, instance):

        token = super(MovesBackend, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token


class MovesAuth(BaseOAuth2, PhysicalBackend):
    """Moves OAuth authentication mechanism"""
    AUTHORIZATION_URL = MOVES_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = MOVES_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = MOVES_ACCESS_TOKEN_URL
    AUTH_BACKEND = MovesBackend
    SETTINGS_KEY_NAME = 'MOVES_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'MOVES_CONSUMER_SECRET'
    
    
    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        token = '?access_token=' + access_token
        root = '/user/profile'
        try:
            return requests.get(MOVES_SERVER + root + token).json()
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        else:
            return super(MovesAuth, self).auth_complete(*args, **kwargs)


# Backend definition
BACKENDS = {
    'moves': MovesAuth,
}
