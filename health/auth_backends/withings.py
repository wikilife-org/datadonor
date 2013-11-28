# coding=utf-8

"""
Withings OAuth 1.0 http://oauth.net/core/1.0/ flow
http://www.withings.com/en/api/oauthguide
"""

from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT
                   
from social_auth.backends import OAuthBackend, HealthBackend, BaseOAuth,\
    ConsumerBasedOAuth


class WithingsBackend(OAuthBackend, HealthBackend):
    """Withings OAuth 1.0 authentication backend"""

    name = 'withings'

    def get_user_id(self, details, response):
        print details
        print response

    def get_user_details(self, response):
        print response
        return {}


class WithingsAuth(ConsumerBasedOAuth):
    """Withings OAuth support"""
    AUTH_BACKEND = WithingsBackend
    SETTINGS_KEY_NAME = 'WITHINGS_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'WITHINGS_CONSUMER_SECRET'
    AUTHORIZATION_URL = 'https://oauth.withings.com/account/authorize'
    REQUEST_TOKEN_URL = 'https://oauth.withings.com/account/request_token'
    ACCESS_TOKEN_URL = 'https://oauth.withings.com/account/access_token'


# Backend definition
BACKENDS = {
    'withings': WithingsAuth,
}
