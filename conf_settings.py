# ========= SOCIAL =======
TWITTER_CONSUMER_KEY ='ZWhTDeIIydZSTtpLDaKLg'     
TWITTER_CONSUMER_SECRET ='geDuzAlLPWX1ywir9jqZQniGg0WAwo76hwlHk'

LINKEDIN_CONSUMER_KEY= 'zis5vcnq0ki2'
LINKEDIN_CONSUMER_SECRET='r4ZZ7wS7o6L74d4s'

FOURSQUARE_CONSUMER_KEY='FQUYFXTJEIYOZ5WXUJSRRBXDUWDGSU3000JSGKKVHQL0I0Q4'
FOURSQUARE_CONSUMER_SECRET='UH1XNR23TOU3JBAOQQILGN1GK1F1Y1JIOZGHZEN3KDNFNNCW'

GOOGLE_OAUTH2_CLIENT_ID= '1088423470480.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'fGLjRWbLpcjNWhXkdchvwxtA'

FACEBOOK_APP_ID ="413830832055733"
FACEBOOK_API_SECRET ="109fe31e8b4aebea9c923b0dda5aa3f8"

#===== END SOCIAL =======#

RUNKEEPER_CONSUMER_KEY = '33116a40224c40708ae6781873fc806e'
RUNKEEPER_CONSUMER_SECRET = '15d05a775c6e4057886ba90b26954855'

DAILYMILE_CONSUMER_KEY = 'P0dp54yhTE72K8v4lY58Lb8fiTSOd5mNfb65kp04'
DAILYMILE_CONSUMER_SECRET = 'raEtLJBtXn3xWu6xopPhqvCwSLLAKKcAEt9cfISo'

IHEALTH_CONSUMER_KEY = '46d14d16679f4abaa8fa9762a9dba955'
IHEALTH_CONSUMER_SECRET = 'bb71b06b8a9e49d19cd3430543b2b135'

JAWBONE_CONSUMER_KEY = 'CU3cmqTl6S0'
JAWBONE_CONSUMER_SECRET = 'fc1bf30245a0bbd30986a79874f8167aab5015b8'
JAWBONE_EXTENDED_PERMISSIONS = ['basic_read', 'extended_read', 'friends_read', 'mood_read', 'sleep_read', 
                                'meal_read', 'weight_read', 'cardiac_read', 'generic_event_read']

ANDME_CLIENT ="36fe7db30c8de9fe66a49a0be37896e5"
ANDME_SECRET ="25009972bce773fb2ab0860773512885"


FITBIT_CONSUMER_KEY="a342fda98477421eaa80ef845713d666"
FITBIT_CONSUMER_SECRET="6917489fb2724bdbadc8d52b54cd809b"

#jquintas keys
#BODYMEDIA_CONSUMER_KEY='njb4mmpzrsjpqwaz3k7u6kg8hxjnzk9r'
#BODYMEDIA_CONSUMER_SECRET='MgypmdPnqP25ahH98g52g3c9Z24KJbTQmmEEGAKQJuhcwPBs8wcT7yaKV69kb4Uf'
#datadonors keys
BODYMEDIA_CONSUMER_KEY = '3dh55bqrxns3pwwqdz59puynvyjvd376'
BODYMEDIA_CONSUMER_SECRET = 'JeTCWwgn6h5mPzUa2JbHRTaGCFHVUNaVtbbjuHXwP9fFeus52ZtXC85VdxrRsgzm'




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
