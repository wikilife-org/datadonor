"""
Moodsy OAuth 2.0 with "Authorization Code" flow
https://developers.moodsy/documentatio/
"""

from social_auth.backends import OAuthBackend, BaseOAuth2, HealthBackend


MOODSY_AUTHORIZATION_URL = "https://developers.moodsy.me/authorize"
"""
This is the URL to which your application should redirect the user in order to authorize access to his or her Moodsy account.
"""

MOODSY_ACCESS_TOKEN_URL = "https://developers.moodsy.me/token"
"""
This is the URL at which your application can convert an authorization code to an access token.
"""


class MoodsyBackend(OAuthBackend, HealthBackend):
    """Moodsy OAuth2 authentication backend"""
    name = 'moodsy'

    def get_user_id(self, details, response):
        #access_token = response["access_token"]
        #token_type = response["token_type"]
        return "id_%s" %response["access_token"]

    def get_user_details(self, response):
        #access_token = response["access_token"]
        #token_type = response["token_type"]
        return {}


class MoodsyAuth(BaseOAuth2, HealthBackend):
    """Moodsy OAuth2 support"""
    AUTHORIZATION_URL = MOODSY_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = MOODSY_ACCESS_TOKEN_URL
    AUTH_BACKEND = MoodsyBackend
    SETTINGS_KEY_NAME = 'MOODSY_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'MOODSY_CONSUMER_SECRET'
    REDIRECT_STATE = False

# Backend definition
BACKENDS = {
    'moodsy': MoodsyAuth,
}
