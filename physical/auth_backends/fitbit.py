# -*- coding: utf-8 -*-

"""
Fitbit OAuth support.

This contribution adds support for Fitbit OAuth service. The settings
FITBIT_CONSUMER_KEY and FITBIT_CONSUMER_SECRET must be defined with the values
given by Fitbit application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
OAuth oauth_consumer_key="b54a8e0fe4314969b52505768c5f1d08",
        oauth_signature_method="HMAC-SHA1",
        oauth_timestamp="1396467353",
        oauth_nonce="2226742294",
        oauth_version="1.0",
        oauth_token="8ccb38077b9b95269bbd4d6e02e48991",
        oauth_signature="ifNNy1XhmVow5xCy%2FmYMrWho8MU%3D"

"""
from social_auth.exceptions import StopPipeline, AuthException, AuthFailed, \
                                   AuthCanceled, AuthUnknownError, \
                                   AuthTokenError, AuthMissingParameter, \
                                   AuthStateMissing, AuthStateForbidden, \
                                   NotAllowedToDisconnect
try:
    from urlparse import parse_qs
    parse_qs  # placate pyflakes
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs

from urllib2 import Request, HTTPError
from django.contrib.auth import authenticate
from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT, urllib
                   
from social_auth.backends import OAuthBackend, NutritionBackend, BaseOAuth,\
    ConsumerBasedOAuth
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, PhysicalBackend
from social_auth.utils import setting, dsa_urlopen
import oauth2 as oauth


import oauth2 as oauth
import requests
import json
import datetime
import urllib

from requests_oauthlib import OAuth1Session

                               


# Fitbit configuration
FITBIT_SERVER = 'https://api.fitbit.com'
FITBIT_REQUEST_TOKEN_URL = '%s/oauth/request_token' % FITBIT_SERVER
FITBIT_AUTHORIZATION_URL = 'https://www.fitbit.com/oauth/authorize'
FITBIT_ACCESS_TOKEN_URL = '%s/oauth/access_token' % FITBIT_SERVER
FITBIT_USERINFO = 'http://api.fitbit.com/1/user/-/profile.json'


class FitbitBackend(OAuthBackend, PhysicalBackend):
    """Fitbit OAuth authentication backend"""
    name = 'fitbit'
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


class FitbitAuth(ConsumerBasedOAuth, PhysicalBackend):
    """Fitbit OAuth authentication mechanism"""
    AUTHORIZATION_URL = FITBIT_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = FITBIT_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = FITBIT_ACCESS_TOKEN_URL
    AUTH_BACKEND = FitbitBackend
    SETTINGS_KEY_NAME = 'FITBIT_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'FITBIT_CONSUMER_SECRET'

    def _request(self, method, url, **kwargs):
        """
        A simple wrapper around requests.
        """
        return requests.request(method, url, **kwargs)

    def access_token(self, token, verifier):
        """Step 4: Given the token from step 1, and the verifier from step 3 (see step 2),
        calls fitbit again and returns an access token object.  Extract .key and .secret
        from that and save them, then pass them as user_key and user_secret in future
        API calls to fitbit to get this user's data.
        """
        client = OAuth1Session(
            self.consumer.key,
            client_secret=self.consumer.secret,
            resource_owner_key=token.key,
            resource_owner_secret=token.secret,
            verifier=verifier)
        response = client.fetch_access_token(self.ACCESS_TOKEN_URL)

        user_id = response['encoded_user_id']
        token = oauth.Token(
            key=response['oauth_token'],
            secret=response['oauth_token_secret'])
        token.user_id = user_id

        return token
    
    def access_token_(self, token):
        """Return request for access token value"""
        # Fitbit is a bit different - it passes user information along with
        # the access token, so temporarily store it to vie the user_data
        # method easy access later in the flow!
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        response = self.fetch_response(request)
        token = Token.from_string(response)
        params = parse_qs(response)

        token.encoded_user_id = params.get('encoded_user_id', [None])[0]
        token.fullname = params.get('fullname', [None])[0]
        token.username = params.get('username', [None])[0]
        return token

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return {
            'id': access_token.user_id,
        }

    
    def oauth_request(self, token, url, extra_params=None):
        consumer = OAuthConsumer(*self.get_key_and_secret())
        """if not method:
            method = 'POST' if data else 'GET'"""
        headers = {}
        request = oauth.Request.from_consumer_and_token(consumer, token, http_method="POST", http_url=url, parameters=extra_params)
        request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer,
                             token)
        headers.update(request.to_header())
        response = self._request("POST", url, data=extra_params,
                                 headers=headers)
        return response.content
    
    
    def oauth_authorization_request_(self, token):
        """Generate OAuth request to authorize token."""
        
        request =  OAuthRequest.from_token_and_callback(
            token=token,
            http_url=self.AUTHORIZATION_URL,
        )
        request.is_form_encoded = True
        consumer = OAuthConsumer(*self.get_key_and_secret())
        request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
        return request
    
    def auth_url(self):
        """Return redirect url"""
        token = self.unauthorized_token()
        name = self.AUTH_BACKEND.name + 'unauthorized_token_name'
        if not isinstance(self.request.session.get(name), list):
            self.request.session[name] = []
        self.request.session[name].append(token.to_string())
        self.request.session.modified = True
        return self.oauth_authorization_request(token).to_url()

    def auth_complete(self, *args, **kwargs):
        """Return user, might be logged in"""
        # Multiple unauthorized tokens are supported (see #521)
        name = self.AUTH_BACKEND.name + 'unauthorized_token_name'
        token = None
        verifier = self.request.GET.get("oauth_verifier") or None
        unauthed_tokens = self.request.session.get(name) or []
        if not unauthed_tokens:
            raise AuthTokenError(self, 'Missing unauthorized token')
        for unauthed_token in unauthed_tokens:
            token = Token.from_string(unauthed_token)
            if token.key == self.data.get('oauth_token', 'no-token'):
                unauthed_tokens = list(set(unauthed_tokens) -
                                       set([unauthed_token]))
                self.request.session[name] = unauthed_tokens
                self.request.session.modified = True
                break
        else:
            raise AuthTokenError(self, 'Incorrect tokens')

        try:
            access_token = self.access_token(token ,verifier)
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        return self.do_auth(access_token, *args, **kwargs)

    def do_auth(self, access_token, *args, **kwargs):
        """Finish the auth process once the access_token was retrieved"""
        if isinstance(access_token, basestring):
            access_token = Token.from_string(access_token)

        data = self.user_data(access_token)
        if data is not None:
            data['access_token'] = access_token.to_string()

        kwargs.update({
            'auth': self,
            'response': data,
            self.AUTH_BACKEND.name: True
        })
        return authenticate(*args, **kwargs)

    def unauthorized_token(self):
        """Return request for unauthorized token (first stage)"""
        request = self.oauth_request(
            token=None,
            url=self.REQUEST_TOKEN_URL,
            extra_params=self.request_token_extra_arguments()
        )
        return Token.from_string(request)

    def oauth_authorization_request(self, token):
        """Generate OAuth request to authorize token."""
        params = self.auth_extra_arguments() or {}
        params.update(self.get_scope_argument())
        return OAuthRequest.from_token_and_callback(
            token=token,
            callback=self.redirect_uri,
            http_url=self.AUTHORIZATION_URL,
            parameters=params
        )


    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        response = dsa_urlopen(request.to_url())
        return '\n'.join(response.readlines())

    """def access_token(self, token):
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        return Token.from_string(self.fetch_response(request))"""

    @property
    def consumer(self):
        """Setups consumer"""
        return OAuthConsumer(*self.get_key_and_secret())
# Backend definition
BACKENDS = {
    'fitbit': FitbitAuth,
}
