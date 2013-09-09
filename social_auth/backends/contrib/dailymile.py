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

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, PhysicalBackend


# Dailymile configuration
DAILYMILE_SERVER = 'https://api.dailymile.com'
DAILYMILE_REQUEST_TOKEN_URL = '%s/oauth/token' % DAILYMILE_SERVER
DAILYMILE_AUTHORIZATION_URL = '%s/oauth/authorize' % DAILYMILE_SERVER
DAILYMILE_ACCESS_TOKEN_URL = '%s/oauth/token' % DAILYMILE_SERVER
#DAILYMILE_USERINFO = 'http://api.fitbit.com/1/user/-/profile.json'


class DailyMileBackend(OAuthBackend):
    """DailyMile OAuth authentication backend"""
    name = 'dailymile'
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


class DailyMileAuth(ConsumerBasedOAuth, PhysicalBackend):
    AUTHORIZATION_URL = DAILYMILE_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = DAILYMILE_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = DAILYMILE_ACCESS_TOKEN_URL
    AUTH_BACKEND = DailyMileBackend
    SETTINGS_KEY_NAME = 'DAILYMILE_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'DAILYMILE_CONSUMER_SECRET'

    def access_token(self, token):
        """Return request for access token value"""
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
    'dailymile': DailyMileAuth,
}
