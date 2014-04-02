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
        return response["access_token"]

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
    

# Backend definition
BACKENDS = {
    'fatsecret': FatsecretAuth,
}
