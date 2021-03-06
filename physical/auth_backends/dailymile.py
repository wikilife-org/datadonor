"""
DailyMile OAuth support.

This contribution adds support for Fitbit OAuth service. The settings
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

from social_auth.backends import BaseOAuth2, ConsumerBasedOAuth, OAuthBackend, PhysicalBackend

from urllib import urlencode
from django.utils import simplejson
import requests
import json

# Dailymile configuration
DAILYMILE_SERVER = 'https://api.dailymile.com'
DAILYMILE_REQUEST_TOKEN_URL = '%s/oauth/token' % DAILYMILE_SERVER
DAILYMILE_AUTHORIZATION_URL = '%s/oauth/authorize' % DAILYMILE_SERVER
DAILYMILE_ACCESS_TOKEN_URL = '%s/oauth/token' % DAILYMILE_SERVER
DAILYMILE_USERINFO = 'https://api.dailymile.com/people/me.json'


class DailyMileBackend(OAuthBackend):
    """DailyMile OAuth authentication backend"""
    name = 'dailymile'
    # Default extra data to store
    #EXTRA_DATA = [('id', 'id'),
    #              ('username', 'username'),
    #              ('expires', 'expires')]


    
    def get_user_id(self, details, response):
        response['id'] = 1 #added to pass this
        return response['id']

    def get_user_details(self, response):
        """Return user details from DailyMile account"""
        return {'username': response['username']}


class DailyMileAuth(BaseOAuth2, PhysicalBackend):
    AUTHORIZATION_URL = DAILYMILE_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = DAILYMILE_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = DAILYMILE_ACCESS_TOKEN_URL
    AUTH_BACKEND = DailyMileBackend
    SETTINGS_KEY_NAME = 'DAILYMILE_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'DAILYMILE_CONSUMER_SECRET'
    REDIRECT_STATE = False


    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = DAILYMILE_USERINFO + '?oauth_token=%s' % access_token
        res = requests.get(url)
        try:
            return json.loads(res.text)
        except ValueError:
            return None
        
    
    def auth_url(self):
        """Return redirect url"""
        if self.STATE_PARAMETER or self.REDIRECT_STATE:
            # Store state in session for further request validation. The state
            # value is passed as state parameter (as specified in OAuth2 spec),
            # but also added to redirect_uri, that way we can still verify the
            # request if the provider doesn't implement the state parameter.
            # Reuse token if any.
            name = self.AUTH_BACKEND.name + '_state'
            state = self.request.session.get(name) or self.state_token()
            self.request.session[self.AUTH_BACKEND.name + '_state'] = state
        else:
            state = None

        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())

        if self.request.META.get('QUERY_STRING'):
            query_string = '&' + self.request.META['QUERY_STRING']
        else:
            query_string = ''

        return self.AUTHORIZATION_URL + '?' + urlencode(params) + query_string


# Backend definition
BACKENDS = {
    'dailymile': DailyMileAuth,
}
