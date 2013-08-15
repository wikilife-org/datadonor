"""
BodyMedia OAuth support.
"""

try:
    from urlparse import parse_qs
    parse_qs  # placate pyflakes
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs

from oauth2 import Token

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, PhysicalBackend


# Bodymedia configuration
BODYMEDIA_SERVER = 'https://api.bodymedia.com'
BODYMEDIA_REQUEST_TOKEN_URL = '%s/oauth/request_token' % BODYMEDIA_SERVER
BODYMEDIA_AUTHORIZATION_URL = '%s/oauth/authorize' % BODYMEDIA_SERVER
BODYMEDIA_ACCESS_TOKEN_URL = '%s/oauth/access_token' % BODYMEDIA_SERVER
BODYMEDIA_USERINFO = 'http://api.bodymedia.com/1/user/-/profile.json'


class BodymediaBackend(OAuthBackend):
    """Bodymedia OAuth authentication backend"""
    name = 'bodymedia'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'),
                  ('username', 'username'),
                  ('expires', 'expires')]

    def get_user_id(self, details, response):
        """
        Bodymedia doesn't provide user data, it must be requested to its API:
            https://wiki.bodymedia.com/display/API/API-Get-User-Info
        """
        return response['id']

    def get_user_details(self, response):
        """Return user details from Bodymedia account"""
        return {'username': response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}


class BodymediaAuth(ConsumerBasedOAuth, PhysicalBackend):
    """Bodymedia OAuth authentication mechanism"""
    AUTHORIZATION_URL = BODYMEDIA_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = BODYMEDIA_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = BODYMEDIA_ACCESS_TOKEN_URL
    AUTH_BACKEND = BodymediaBackend
    SETTINGS_KEY_NAME = 'BODYMEDIA_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'BODYMEDIA_CONSUMER_SECRET'

    def access_token(self, token):
        """Return request for access token value"""
        # Bodymedia is a bit different - it passes user information along with
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
            'id': access_token.encoded_user_id,
            'username': access_token.username,
            'fullname': access_token.fullname,
        }


# Backend definition
BACKENDS = {
    'bodymedia': BodymediaAuth,
}
