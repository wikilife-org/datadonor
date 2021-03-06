from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client

from django.utils import simplejson

from social_auth.models import UserSocialAuth
from social_auth.utils import dsa_urlopen


def consumer_oauth_url_request(backend, url, user_or_id, redirect_uri='/',
                               json=True):
    """Builds and retrieves an OAuth signed response."""
    user = UserSocialAuth.resolve_user_or_id(user_or_id)
    oauth_info = user.social_auth.filter(provider=backend.AUTH_BACKEND.name)[0]
    token = Token.from_string(oauth_info.tokens['access_token'])
    request = build_consumer_oauth_request(backend, token, url, redirect_uri)
    response = '\n'.join(dsa_urlopen(request.to_url()).readlines())

    if json:
        response = simplejson.loads(response)
    return response


def build_consumer_oauth_request(backend, token, url, redirect_uri='/',
                                 oauth_verifier=None, extra_params=None,
                                 method=HTTP_METHOD):
    """Builds a Consumer OAuth request."""
    params = {'oauth_callback': redirect_uri}
    if extra_params:
        params.update(extra_params)

    if oauth_verifier:
        params['oauth_verifier'] = oauth_verifier

    consumer = OAuthConsumer(*backend.get_key_and_secret())
    request = OAuthRequest.from_consumer_and_token(consumer,
                                                   token=token,
                                                   http_method=method,
                                                   http_url=url,
                                                   parameters=params)
    request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
    return request

def oauth_req(backend, token, url, http_method="GET", post_body=None,
        http_headers=None):
    consumer = OAuthConsumer(*backend.get_key_and_secret())
    token = Token.from_string(token)
    client = Client(consumer, token)
 
    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers,
        force_auth_header=True
    )
    return content