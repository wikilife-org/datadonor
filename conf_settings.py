TWITTER_CONSUMER_KEY = 'kbftZoPPtKFqNvqo4XFg'                                # application ID
TWITTER_CONSUMER_SECRET = 'YbD5Rkv0BzDSBbrxBfXQNQ3Bf0jqPTTBYNi325huMc'                            # application secret key

FACEBOOK_APP_ID = "167345460113739"
FACEBOOK_APP_SECRET = "56fe36cce6798c4655fdb55827551b36"

FITBIT_CONSUMER_KEY="bc768a08267e47eb918ab8abb43b9ade"
FITBIT_CONSUMER_SECRET="d980c6b66b184eaebf3b4809c1392702"

LINKEDIN_CONSUMER_KEY             = ''
LINKEDIN_CONSUMER_SECRET          = ''
SKYROCK_CONSUMER_KEY              = ''
SKYROCK_CONSUMER_SECRET           = ''
ORKUT_CONSUMER_KEY                = ''
ORKUT_CONSUMER_SECRET             = ''
GOOGLE_OAUTH2_CLIENT_ID           = ''
GOOGLE_OAUTH2_CLIENT_SECRET       = ''
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME      = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
LOGIN_ERROR_URL                   = '/login/error/'
VKONTAKTE_APP_ID                  = ''
VKONTAKTE_APP_SECRET              = ''
# Usage for applications auth: {'key': application_key, 'user_mode': 0 (default) | 1 (check) | 2 (online check) }
# 0 means is_app_user request parameter is ignored, 1 - must be = 1, 2 - checked via VK API request (useful when user
# connects to your application on app page and you reload the iframe)
VKONTAKTE_APP_AUTH                = None
ODNOKLASSNIKI_OAUTH2_CLIENT_KEY   = ''
ODNOKLASSNIKI_OAUTH2_APP_KEY      = ''
ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET = ''
MAILRU_OAUTH2_CLIENT_KEY   		  = ''
MAILRU_OAUTH2_APP_KEY      		  = ''
MAILRU_OAUTH2_CLIENT_SECRET       = ''
#SOCIAL_AUTH_USER_MODEL           = 'app.CustomUser'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
GITHUB_APP_ID                     = ''
GITHUB_API_SECRET                 = ''
FOURSQUARE_CONSUMER_KEY           = ''
FOURSQUARE_CONSUMER_SECRET        = ''
DOUBAN_CONSUMER_KEY               = ''
DOUBAN_CONSUMER_SECRET            = ''
YANDEX_OAUTH2_CLIENT_KEY          = ''
YANDEX_OAUTH2_CLIENT_SECRET       = ''
YANDEX_OAUTH2_API_URL             = 'https://api-yaru.yandex.ru/me/' # http://api.moikrug.ru/v1/my/ for Moi Krug
DAILYMOTION_OAUTH2_KEY            = ''
DAILYMOTION_OAUTH2_SECRET         = ''
SHOPIFY_APP_API_KEY                 = ''
SHOPIFY_SHARED_SECRET             = ''
STOCKTWITS_CONSUMER_KEY           = ''
STOCKTWITS_CONSUMER_SECRET        = ''
READABILITY_CONSUMER_KEY          = ''
READABILITY_CONSUMER_SECRET       = ''

# Backward compatibility
YANDEX_APP_ID = YANDEX_OAUTH2_CLIENT_KEY
YANDEX_API_SECRET = YANDEX_OAUTH2_CLIENT_SECRET

VK_APP_ID = VKONTAKTE_APP_ID
VK_API_SECRET = VKONTAKTE_APP_SECRET
# VKONTAKTE_APP_AUTH={'key':'iframe_app_secret_key', 'user_mode': 2, 'id':'iframe_app_id'}

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'social.pipeline.redirect_to_form',
    'social.pipeline.username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)
