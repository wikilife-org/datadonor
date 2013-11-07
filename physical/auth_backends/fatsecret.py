# coding=utf-8

"""
Fatsecret OAuth 1.0 http://oauth.net/core/1.0/ flow
http://platform.fatsecret.com/api/Default.aspx?screen=rapiauth#correctly_signing
"""

from social_auth.backends import OAuthBackend, PhysicalBackend, BaseOAuth,\
    ConsumerBasedOAuth


class FatsecretBackend(OAuthBackend, PhysicalBackend):
    """Fatsecret OAuth 1.0 authentication backend"""

    name = 'fatsecret'

    def get_user_id(self, details, response):
        print details
        print response

    def get_user_details(self, response):
        print response
        return {}


class FatsecretAuth(ConsumerBasedOAuth):
    """Fatsecret OAuth support"""
    AUTH_BACKEND = FatsecretBackend
    SETTINGS_KEY_NAME = 'FATSECRET_REST_API_ACCESS_KEY'
    SETTINGS_SECRET_NAME = 'FATSECRET_REST_API_SHARED_SECRET'
    AUTHORIZATION_URL = 'http://www.fatsecret.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.fatsecret.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'http://www.fatsecret.com/oauth/access_token'


# Backend definition
BACKENDS = {
    'fatsecret': FatsecretAuth,
}
