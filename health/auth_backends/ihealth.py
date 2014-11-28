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

from social_auth.backends import BaseOAuth2, ConsumerBasedOAuth, OAuthBackend, HealthBackend

from urllib import urlencode
from django.utils import simplejson
import requests
import json
from urllib2 import Request, HTTPError
from  social_auth.utils import dsa_urlopen

IHEALTH_SERVER = 'https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2'
IHEALTH_REQUEST_TOKEN_URL = '%s/userauthorization' % IHEALTH_SERVER
IHEALTH_AUTHORIZATION_URL = '%s/userauthorization' % IHEALTH_SERVER
IHEALTH_ACCESS_TOKEN_URL = '%s/userauthorization' % IHEALTH_SERVER
#IHEALTH_USERINFO = 'https://api.dailymile.com/people/me.json'


class IhealthBackend(OAuthBackend):
    """ihealth OAuth authentication backend"""
    name = 'ihealth'
    
    
    def get_user_id(self, details, response):
        return response['UserID']

    def get_user_details(self, response):
        """Return user details from ihealth account"""
        return {'username': response['UserID']}


class IhealthAuth(BaseOAuth2, PhysicalBackend):
    AUTHORIZATION_URL = IHEALTH_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = IHEALTH_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = IHEALTH_ACCESS_TOKEN_URL
    AUTH_BACKEND = IhealthBackend
    SETTINGS_KEY_NAME = 'IHEALTH_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'IHEALTH_CONSUMER_SECRET'
    REDIRECT_STATE = False
    STATE_PARAMETER = False


    def user_data_(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = DAILYMILE_USERINFO + '?oauth_token=%s' % access_token
        res = requests.get(url)
        try:
            return json.loads(res.text)
        except ValueError:
            return None
        
    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())
        response = requests.request("GET", self.ACCESS_TOKEN_URL, params=params )
        #request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params), headers=self.auth_headers())

        try:
            response = response.json()
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['AccessToken'], response=response,
                            *args, **kwargs)
        
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
            
        #params['APIName'] = 'OpenApiBP OpenApiActivity OpenApiBG OpenApiSleep OpenApiUserInfo OpenApiWeight'
        aPIName = 'OpenApiBP OpenApiActivity OpenApiBG OpenApiSleep OpenApiUserInfo OpenApiWeight'

        return self.AUTHORIZATION_URL + '?' + urlencode(params) + query_string + "&APIName=" + aPIName

# Backend definition
BACKENDS = {
    'ihealth': IhealthAuth,
}
