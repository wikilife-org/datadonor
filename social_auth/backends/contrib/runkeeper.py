"""
Runkeeper OAuth support.

This contribution adds support for RunkeeperAuth OAuth service. The settings
FITBIT_CONSUMER_KEY and FITBIT_CONSUMER_SECRET must be defined with the values
given by Fitbit application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
"""
try:
    from urlparse import parse_qs
    parse_qs  # placate pyflakes
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs

from oauth2 import Token

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, PhysicalBackend


import requests
import urllib

# Runkeeper configuration
RUNKEEPER_SERVER = 'https://api.runkeeper.com'
RUNKEEPER_REQUEST_TOKEN_URL = '%s/oauth/request_token' % RUNKEEPER_SERVER
RUNKEEPER_AUTHORIZATION_URL = '%s/apps/authorize' % RUNKEEPER_SERVER
RUNKEEPER_ACCESS_TOKEN_URL = '%s/apps/token' % RUNKEEPER_SERVER
RUNKEEPER_USERINFO = 'http://api.runkeeper.com/1/user/-/profile.json'
RUNKEEPER_REDIRECT_URL = 'http://127.0.0.1:8000/rk'

class RunkeeperBackend(OAuthBackend):
    """Runkeeper OAuth authentication backend"""
    name = 'runkeeper'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'),
                  ('username', 'username'),
                  ('expires', 'expires')]

    def get_user_id(self, details, response):
        """
        Fitbit doesn't provide user data, it must be requested to its API:
            https://wiki.fitbit.com/display/API/API-Get-User-Info
        """
        return response['id']

    def get_user_details(self, response):
        """Return user details from Fitbit account"""
        return {'username': response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}


class RunkeeperAuth(ConsumerBasedOAuth, PhysicalBackend):
    """Runkeeper OAuth authentication mechanism"""
    AUTHORIZATION_URL = RUNKEEPER_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = RUNKEEPER_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = RUNKEEPER_ACCESS_TOKEN_URL
    AUTH_BACKEND = RunkeeperBackend
    SETTINGS_KEY_NAME = 'RUNKEEPER_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'RUNKEEPER_CONSUMER_SECRET'


    def access_token(self, token):
        """Returns Access Token retrieved from the Health Graph API Token
        Endpoint following the login to RunKeeper.

        @param code: Code returned by Health Graph API at the Authorization or
                     RunKeeper Login phase.
        @return:     Access Token for querying the Health Graph API.

        """
        payload = {'grant_type': 'authorization_code',
                   'code': code,
                   'client_id': SETTINGS_KEY_NAME,
                   'client_secret': SETTINGS_SECRET_NAME,
                   'redirect_uri': RUNKEEPER_REDIRECT_URL,}
        req = requests.post(ACCESS_TOKEN_URL, data=payload)
        data = req.json()
        return data.get('access_token')

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return {
            'id': access_token.encoded_user_id,
            'username': access_token.username,
            'fullname': access_token.fullname,
        }


# Backend definition
BACKENDS = {
    'runkeeper': RunkeeperAuth,
}