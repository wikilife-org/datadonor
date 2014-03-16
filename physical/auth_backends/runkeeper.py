"""
Runkeeper OAuth 2.0 with "Authorization Code" flow
http://developer.runkeeper.com/healthgraph/getting-started
"""

from social_auth.backends import OAuthBackend, BaseOAuth2, PhysicalBackend


RUNKEEPER_AUTHORIZATION_URL = "https://runkeeper.com/apps/authorize"
"""
This is the URL to which your application should redirect the user in order to authorize access to his or her RunKeeper account.
"""

RUNKEEPER_ACCESS_TOKEN_URL = "https://runkeeper.com/apps/token"
"""
This is the URL at which your application can convert an authorization code to an access token.
"""

RUNKEEPER_DEAUTHORIZATION_URL = "https://runkeeper.com/apps/de-authorize"
"""
This is the URL at which your application can disconnect itself from the user's account.
"""


class RunkeeperBackend(OAuthBackend, PhysicalBackend):
    """Runkeeper OAuth2 authentication backend"""
    name = 'runkeeper'

    def get_user_id(self, details, response):
        #access_token = response["access_token"]
        #token_type = response["token_type"]
        return "id_%s" %response["access_token"]

    def get_user_details(self, response):
        #access_token = response["access_token"]
        #token_type = response["token_type"]
        return {}


class RunkeeperAuth(BaseOAuth2, PhysicalBackend):
    """Runkeeper OAuth2 support"""
    AUTHORIZATION_URL = RUNKEEPER_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = RUNKEEPER_ACCESS_TOKEN_URL
    AUTH_BACKEND = RunkeeperBackend
    SETTINGS_KEY_NAME = 'RUNKEEPER_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'RUNKEEPER_CLIENT_SECRET'


# Backend definition
BACKENDS = {
    'runkeeper': RunkeeperAuth,
}
