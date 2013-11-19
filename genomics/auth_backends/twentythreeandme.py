"""
23andMe OAuth 2.0 with "Authorization Code" flow
https://api.23andme.com/docs/authentication/
"""

from social_auth.backends import OAuthBackend, BaseOAuth2, GenomicsBackend


TWENTYTHREEMEANDME_AUTHORIZATION_URL = "https://api.23andme.com/authorize"
"""
This is the URL to which your application should redirect the user in order to authorize access to his or her 23andMe account.
"""

TWENTYTHREEMEANDME_ACCESS_TOKEN_URL = "https://api.23andme.com/token"
"""
This is the URL at which your application can convert an authorization code to an access token.
"""


class TwentyThreeAndMeBackend(OAuthBackend, GenomicsBackend):
    """23andMe OAuth2 authentication backend"""
    name = 'twentythreeandme'

    def get_user_id(self, details, response):
        #access_token = response["access_token"]
        #token_type = response["token_type"]
        return "id_%s" %response["access_token"]

    def get_user_details(self, response):
        #access_token = response["access_token"]
        #token_type = response["token_type"]
        return {}


class TwentyThreeAndMeAuth(BaseOAuth2):
    """23andMe OAuth2 support"""
    AUTHORIZATION_URL = TWENTYTHREEMEANDME_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = TWENTYTHREEMEANDME_ACCESS_TOKEN_URL
    AUTH_BACKEND = TwentyThreeAndMeBackend
    SETTINGS_KEY_NAME = 'TWENTYTHREEMEANDME_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'TWENTYTHREEMEANDME_CLIENT_SECRET'
    SCOPE_VAR_NAME = "basic genomes haplogroups ancestry relatives analyses profile introduction names rs53576 rs1815739 rs6152 rs1800497 rs1805007 rs9939609 rs662799 rs7495174 rs7903146 rs12255372 rs1799971 rs17822931 rs4680 rs1333049 rs1801133 rs1051730 rs3750344 rs4988235"





# Backend definition
BACKENDS = {
    'twentythreeandme': TwentyThreeAndMeAuth,
}
