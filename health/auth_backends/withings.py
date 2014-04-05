# coding=utf-8

"""
Withings OAuth 1.0 http://oauth.net/core/1.0/ flow
http://www.withings.com/en/api/oauthguide
"""

from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT
                   
from social_auth.backends import OAuthBackend, HealthBackend, BaseOAuth,\
    ConsumerBasedOAuth

from social_auth.utils import setting
PIPELINE = setting('SOCIAL_AUTH_PIPELINE', (
                'social_auth.backends.pipeline.social.social_auth_user',
                # Removed by default since it can be a dangerouse behavior that
                # could lead to accounts take over.
                #'social_auth.backends.pipeline.associate.associate_by_email',
                'social_auth.backends.pipeline.user.get_username',
                'social_auth.backends.pipeline.user.create_user',
                'social_auth.backends.pipeline.social.associate_user',
                'social_auth.backends.pipeline.social.load_extra_data',
                'social_auth.backends.pipeline.user.update_user_details',
           ))

class WithingsBackend(OAuthBackend, HealthBackend):
    """Withings OAuth 1.0 authentication backend"""

    name = 'withings'


    def authenticate(self, *args, **kwargs):
        """Authenticate user using social credentials

        Authentication is made if this is the correct backend, backend
        verification is made by kwargs inspection for current backend
        name presence.
        """
        # Validate backend and arguments. Require that the Social Auth
        # response be passed in as a keyword argument, to make sure we
        # don't match the username/password calling conventions of
        # authenticate.
        if not (self.name and kwargs.get(self.name) and 'response' in kwargs):
            return None

        response = kwargs.get('response')
        pipeline = PIPELINE
        kwargs = kwargs.copy()
        kwargs['backend'] = self

        if 'pipeline_index' in kwargs:
            pipeline = pipeline[kwargs['pipeline_index']:]
        else:
            kwargs['details'] = self.get_user_details(response)
            kwargs['uid'] = self.get_user_id(kwargs['request'])
            kwargs['is_new'] = False
                
        out = self.pipeline(pipeline, *args, **kwargs)
        if not isinstance(out, dict):
            return out

        social_user = out.get('social_user')
        if social_user:
            # define user.social_user attribute to track current social
            # account
            user = social_user.user
            user.social_user = social_user
            user.is_new = out.get('is_new')
            return user
        
    def get_user_id(self, request):
        
        return request.GET["userid"]

    def get_user_details(self, response):
        return {}


class WithingsAuth(ConsumerBasedOAuth, HealthBackend):
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
