# coding=utf-8

"""
Fatsecret OAuth 1.0 http://oauth.net/core/1.0/ flow
http://platform.fatsecret.com/api/Default.aspx?screen=rapiauth#correctly_signing
"""

from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT
                   
from social_auth.backends import OAuthBackend, NutritionBackend, BaseOAuth,\
    ConsumerBasedOAuth


class FatsecretBackend(OAuthBackend, NutritionBackend):
    """Fatsecret OAuth 1.0 authentication backend"""

    name = 'fatsecret'

    def get_user_id(self, details, response):
        print details
        print response

    def get_user_details(self, response):
        print response
        return {}


class FatsecretAuth(ConsumerBasedOAuth, NutritionBackend):
    """Fatsecret OAuth support"""
    AUTH_BACKEND = FatsecretBackend
    SETTINGS_KEY_NAME = 'FATSECRET_REST_API_ACCESS_KEY'
    SETTINGS_SECRET_NAME = 'FATSECRET_REST_API_SHARED_SECRET'
    AUTHORIZATION_URL = 'http://www.fatsecret.com/oauth/authorize'
    #REQUEST_TOKEN_URL = 'http://platform.fatsecret.com/rest/server.api/oauth/request_token'
    REQUEST_TOKEN_URL = 'http://www.fatsecret.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'http://www.fatsecret.com/oauth/access_token'

    def oauth_request(self, token, url, extra_params=None):

        if not token:
            params = {'oauth_callback': self.redirect_uri,
                  "method": "profile.get_auth"}
        else:
            params = {"method": "profile.get_auth"}
        if extra_params:
            params.update(extra_params)
        
        oauth_verifier = self.data.get('oauth_verifier')
        if oauth_verifier:
            params['oauth_verifier'] = oauth_verifier
    
        consumer = OAuthConsumer(*self.get_key_and_secret())
        request = OAuthRequest.from_consumer_and_token(consumer,
                                                       token=token,
                                                       http_method="GET",
                                                       http_url=url,
                                                       parameters=params,
                                                       is_form_encoded=True)
        request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
        return request

    def oauth_authorization_request(self, token):
        """Generate OAuth request to authorize token."""
        params = self.auth_extra_arguments() or {}
        params.update(self.get_scope_argument())
        params.update({"oauth_nonce":OAuthRequest.make_nonce()})
        params.update({"oauth_timestamp":OAuthRequest.make_timestamp()})
        params.update({"method": "profile.get_auth"})
        
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
    
    def oauth_request_(self, token, url, extra_params=None):
        #extra_params["method"] = "profile.request_script_session_key"

        request.pop("oauth_body_hash")

        #consumer_secret = "a781b6c7f9b44255a2acbb70b914fbe1"
        #request["oauth_signature"] = self._get_oauth_signature(request, consumer_secret, token)
        #request["method"]= "profile.request_script_session_key"
        return request

    
    """
    def _get_oauth_signature(self, request, consumer_secret, token):
        from oauth2 import Token, escape
        import hmac
        import binascii
        try:
            from hashlib import sha1
            sha = sha1
        except ImportError:
            # hashlib was added in Python 2.5
            import sha
        
        if not hasattr(request, 'normalized_url') or request.normalized_url is None:
            raise ValueError("Base URL for request is not set.")

        sig = (
            escape(request.method),
            escape(request.normalized_url),
            escape(request.get_normalized_parameters()),
        )

        key = '%s&' % escape(consumer_secret)
        if token:
            key += escape(token.secret)
        raw = ' & '.join(sig)
        
        hashed = hmac.new(key, raw, sha)

        # Calculate the digest base 64.
        return binascii.b2a_base64(hashed.digest())[:-1]
    """


class FatBackend(OAuthBackend, NutritionBackend):
    """Twitter OAuth authentication backend"""
    name = 'fatsecret'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        try:
            first_name, last_name = response['name'].split(' ', 1)
        except:
            first_name = response['name']
            last_name = ''
        return {'username': response['screen_name'],
                'email': '',  # not supplied
                'fullname': response['name'],
                'first_name': first_name,
                'last_name': last_name}

    @classmethod
    def tokens(cls, instance):
        """Return the tokens needed to authenticate the access to any API the
        service might provide. Twitter uses a pair of OAuthToken consisting of
        an oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(FatBackend, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token

from urllib import urlopen

from oauth2 import Request as OAuthRequest, Token as OAuthToken, \
                   SignatureMethod_HMAC_SHA1

from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth
from social_auth.backends import OAuthBackend

class FatAuth(ConsumerBasedOAuth, NutritionBackend):

    AUTH_BACKEND = FatBackend
    SETTINGS_KEY_NAME = 'FATSECRET_REST_API_ACCESS_KEY'
    SETTINGS_SECRET_NAME = 'FATSECRET_REST_API_SHARED_SECRET'
    AUTHORIZATION_URL = 'http://www.fatsecret.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.fatsecret.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'http://www.fatsecret.com/oauth/access_token'
    
    
    def oauth_request(self, token, url, extra_params=None):
        params = {
            'oauth_callback': self.redirect_uri,
        }

        if extra_params:
            params.update(extra_params)

        if 'oauth_verifier' in self.data:
            params['oauth_verifier'] = self.data['oauth_verifier']

        request = OAuthRequest.from_consumer_and_token(self.consumer,
                                                       token=token,
                                                       http_url=url,
                                                       parameters=params)
        request.sign_request(SignatureMethod_HMAC_SHA1(), self.consumer, token)
        request.pop("oauth_body_hash")
        return request

    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        response = urlopen(request.to_url())
        return response.read()
#

# Backend definition
BACKENDS = {
    'fatsecret': FatsecretAuth,
}
