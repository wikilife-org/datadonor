"""
Moodpanda OAuth support
"""
from social_auth.backends import BaseOAuth2, ConsumerBasedOAuth, OAuthBackend, HealthBackend

class MoodPandaBackend(OAuthBackend):
    """MoodPanda dummy authentication backend"""
    name = 'moodpanda'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        pass
    

class MoodPandaAuth(BaseOAuth2, HealthBackend):
    AUTHORIZATION_URL = ""
    REQUEST_TOKEN_URL = ""
    ACCESS_TOKEN_URL = ""
    SETTINGS_KEY_NAME = 'MOOD_PANDA_KEY'
    SETTINGS_SECRET_NAME = 'MOOD_PANDA_SECRET_KEY'
    AUTH_BACKEND = MoodPandaBackend


    def user_data(self, access_token, *args, **kwargs):
        pass

    def auth_complete(self, *args, **kwargs):
        pass

# Backend definition
BACKENDS = {
    'moodpanda': MoodPandaAuth,
}
