"""
Fitbit OAuth support.

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

from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT, urllib
                   
from social_auth.backends import OAuthBackend, NutritionBackend, BaseOAuth,\
    ConsumerBasedOAuth
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, PhysicalBackend
from social_auth.utils import setting, dsa_urlopen
import oauth2 as oauth


# Fitbit configuration
FITBIT_SERVER = 'https://api.fitbit.com'
FITBIT_REQUEST_TOKEN_URL = '%s/oauth/request_token' % FITBIT_SERVER
FITBIT_AUTHORIZATION_URL = 'https://www.fitbit.com/oauth/authorize'
FITBIT_ACCESS_TOKEN_URL = '%s/oauth/access_token' % FITBIT_SERVER
FITBIT_USERINFO = 'http://api.fitbit.com/1/user/-/profile.json'


class FitbitBackend(OAuthBackend):
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

    def access_token(self, token):
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
            'id': access_token.encoded_user_id,
            'username': access_token.username,
            'fullname': access_token.fullname,
        }

    
    def oauth_request(self, token, url, extra_params=None):
        """if token:
            token = Token.from_string(token)"""
        params = self.auth_extra_arguments() or {}
        params.update(self.get_scope_argument())
        params.update({"oauth_nonce":OAuthRequest.make_nonce()})
        params.update({"oauth_timestamp":OAuthRequest.make_timestamp()})
        params.update({"oauth_version": "1.0"})
        if not token:
            params.update({'oauth_callback': self.redirect_uri})
        consumer = OAuthConsumer(*self.get_key_and_secret())
        client = oauth.Client(consumer, token)
        body = urllib.urlencode(params)
        client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())
 
        auth_header = "OAuth oauth_consumer_key=%s&%s"%(setting(self.SETTINGS_KEY_NAME), body)
        # and launch the request
        resp, content = client.request(url, "POST", body=body, headers={'Authorization': auth_header})
        if resp['status'] != '200':
            print content
            raise Exception("Invalid response from Fitbit.")

        # return the interpreted data
        return content
    
    def oauth_request_(self, token, url, extra_params=None):



        if extra_params:
            params.update(extra_params)
        
        oauth_verifier = self.data.get('oauth_verifier')
        if oauth_verifier:
            params['oauth_verifier'] = oauth_verifier
    
        consumer = OAuthConsumer(*self.get_key_and_secret())
        request = OAuthRequest.from_consumer_and_token(consumer,
                                                       token=token,
                                                       http_method="POST",
                                                       http_url=url,
                                                       parameters=params,
                                                       is_form_encoded=True)
        request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
        
        return request

    def unauthorized_token(self):
        """Return request for unauthorized token (first stage)"""
        response = self.oauth_request(
            token=None,
            url=self.REQUEST_TOKEN_URL,
            extra_params=self.request_token_extra_arguments()
        )
        return Token.from_string(response)

    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        response = dsa_urlopen(request.to_postdata())
        return '\n'.join(response.readlines())
    
    def oauth_authorization_request(self, token):
        """Generate OAuth request to authorize token."""
        params = self.auth_extra_arguments() or {}
        params.update(self.get_scope_argument())
        params.update({"oauth_nonce":OAuthRequest.make_nonce()})
        params.update({"oauth_timestamp":OAuthRequest.make_timestamp()})
        params.update({"oauth_version": "1.0"})
        
        request =  OAuthRequest.from_token_and_callback(
            token=token,
            callback=self.redirect_uri,
            http_url=self.AUTHORIZATION_URL,
            parameters=params
        )
        request.is_form_encoded = True
        consumer = OAuthConsumer(*self.get_key_and_secret())
        request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
        return request
# Backend definition
BACKENDS = {
    'fitbit': FitbitAuth,
}
