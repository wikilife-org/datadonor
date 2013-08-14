TWITTER_CONSUMER_KEY = 'kbftZoPPtKFqNvqo4XFg'                                # application ID
TWITTER_CONSUMER_SECRET = 'YbD5Rkv0BzDSBbrxBfXQNQ3Bf0jqPTTBYNi325huMc'                            # application secret key

FACEBOOK_APP_ID = "167345460113739"
FACEBOOK_API_SECRET = "56fe36cce6798c4655fdb55827551b36"

FITBIT_CONSUMER_KEY="a342fda98477421eaa80ef845713d666"
FITBIT_CONSUMER_SECRET="6917489fb2724bdbadc8d52b54cd809b"

LINKEDIN_CONSUMER_KEY= 'bhq566fxpdov'
LINKEDIN_CONSUMER_SECRET='Xm1ec4cP6s31dbEk'

FOURSQUARE_CONSUMER_KEY='EFL0LHHBGHTE1M35RLXMZ3AP0A15QWTPKXA4LCOMMYHYGSIB'
FOURSQUARE_CONSUMER_SECRET='P1FVCYINNTZRSMLTBD0SK1HNZJZDJW5SDTATYNF5NPMM2HNO'

#PROD
GOOGLE_OAUTH2_CLIENT_ID= '341147010289.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'UsgAGWOFqsJCj_mYbOMmx0AV'

#LOCAL
#GOOGLE_OAUTH2_CLIENT_ID= "341147010289-tbqnl7mrhk961648co2h4h1ckdi93vm8.apps.googleusercontent.com"
#GOOGLE_OAUTH2_CLIENT_SECRET = "7OgQLd2iFyWrbQ1M9hacsdZT"

EVERNOTE_CONSUMER_KEY = 'joaco-quintas'
EVERNOTE_CONSUMER_SECRET = '2598d741657d00de'

RUNKEEPER_CONSUMER_KEY = 'joaco-quintas'
RUNKEEPER_CONSUMER_SECRET = '2598d741657d00de'

BODYMEDIA_CONSUMER_KEY='njb4mmpzrsjpqwaz3k7u6kg8hxjnzk9r'
BODYMEDIA_CONSUMER_SECRET='MgypmdPnqP25ahH98g52g3c9Z24KJbTQmmEEGAKQJuhcwPBs8wcT7yaKV69kb4Uf'

SKYROCK_CONSUMER_KEY              = ''
SKYROCK_CONSUMER_SECRET           = ''
ORKUT_CONSUMER_KEY                = ''
ORKUT_CONSUMER_SECRET             = ''

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

SOCIAL_AUTH_FORCE_POST_DISCONNECT = False
