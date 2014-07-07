from os.path import abspath, dirname, basename, join
from django.utils.translation import ugettext_lazy as _

try:
    import social_auth
except ImportError:
    import sys
    sys.path.insert(0, '..')


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)

ADMINS = (
     ('Joaquin Quintas', 'jquintas@wikilife.org'),
)

import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/var/www/media/elearning/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media").replace('\\','/')
LOCALE_PATHS = (os.path.join(PROJECT_DIR, "locale").replace('\\','/'),)
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ""

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

WELCOME_EMAIL_FROM = "hello@datadonors.org"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

LOGIN_URL = "/"

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'datadonor',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'datadonor',
        'PASSWORD': 'jJwZLUtFL1fR2',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

TIME_ZONE = 'America/Chicago'
#LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True



STATICFILES_DIRS = (
                   os.path.abspath(os.path.join(PROJECT_DIR, 'static')).replace('\\','/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '_u6ym67ywnj0ugi2=6f-a_361i6o5elx91hftz$+klw)(*pqjw'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'middleware.XsSharing',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'social_auth',
    'social',
    'genomics',
    'health',
    'physical',
    'users',
    'nutrition',
    'reports',
    'data'


)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'social.auth_backends.facebook.FacebookBackend',
    'social.auth_backends.twitter.TwitterBackend',
    'social.auth_backends.google.GoogleOAuth2Backend',
    'social.auth_backends.linkedin.LinkedinOAuth2Backend',
    'social.auth_backends.foursquare.FoursquareBackend',
    'physical.auth_backends.runkeeper.RunkeeperBackend',
    'nutrition.auth_backends.fatsecret.FatsecretBackend',
    'genomics.auth_backends.twentythreeandme.TwentyThreeAndMeBackend',
    'physical.auth_backends.dailymile.DailyMileBackend',
    'physical.auth_backends.bodymedia.BodymediaBackend',
    'physical.auth_backends.jawbone.JawboneBackend',
    'physical.auth_backends.moves.MovesBackend',
    'health.auth_backends.moodpanda.MoodPandaBackend',
    'physical.auth_backends.fitbit.FitbitBackend',
    'health.auth_backends.withings.WithingsBackend',    
    'health.auth_backends.ihealth.IhealthBackend',

    'django.contrib.auth.backends.ModelBackend',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_backends',
)

LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"

#TODO rename to AUTH_PIPELINE
SOCIAL_AUTH_PIPELINE = (

    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'pipeline.auth.username',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'pipeline.auth.first_name',

    'pipeline.facebook.facebook_info',
    'pipeline.foursquare.foursquare_info',
    'pipeline.twitter.twitter_info',
    'pipeline.linkedin.linkedin_info',
    'pipeline.google.google_info',
    'pipeline.evernote.evernote_info',
    'pipeline.fitbit.fitbit_info',
    'pipeline.moves.moves_info',
    'pipeline.runkeeper.runkeeper_info',
    'pipeline.fatsecret.fatsecret_info',
    'pipeline.dailymile.dailymile_info',
    'pipeline.ihealth.ihealth_info',
    'pipeline.jawbone.jawbone_info',
    'pipeline.bodymedia.bodymedia_info',
    'pipeline.twentythreeandme.twentythreeandme_info',
    'pipeline.withings.withings_info',
    'pipeline.meta_association.association_info'
)

SOCIAL_AUTH_PIPELINE_old = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    #'social.pipeline.redirect_to_form',
    'social.pipeline.username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    #'social.pipeline.redirect_to_form2',
    'social.pipeline.first_name',
    #'pipeline.twitter.twitter_info',
    #'pipeline.facebook.facebook_info',

)


PROFILE_SOURCES_PRIORITY = {
    "runkeeper": 8,
    "fitbit": 6,
    "fatsecret": 7,
    "facebook": 1,
    "twitter": 4 ,
    "google":2,
    "linkedin":3,
    "foursquare":5,
    "twentythreeandme":9
}

#FACEBOOK CONFIG

FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_about_me', 'user_likes', "read_stream"]
GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
                       'https://www.googleapis.com/auth/userinfo.profile',
                       'https://www.google.com/calendar/feeds',
                       'https://www.googleapis.com/auth/plus.login',
                       'https://www.googleapis.com/auth/plus.me'
                       #'https://www.googleapis.com/auth/people.list',
                       ]

LINKEDIN_SCOPE = ["r_fullprofile", "r_emailaddress", "r_network", "r_contactinfo", "r_basicprofile"]

TWENTYTHREEANDME_SCOPE = ["basic", "genomes", "haplogroups", "ancestry", "relatives", "analyses", "profile:read", "introduction:read", "names", "rs53576", "rs1815739", "rs6152", "rs1800497", "rs1805007", "rs9939609", "rs662799", "rs7495174", "rs7903146", "rs12255372", "rs1799971" ,"rs17822931" ,"rs4680", "rs1333049", "rs1801133" ,"rs1051730" ,"rs3750344", "rs4988235"]

try:
    from conf_settings import *
except:
    pass


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_BACKEND = "social_auth.backends.contrib.django_smtp_ssl.SSLEmailBackend"

#EMAIL_BACKEND = 'django_ses.SESBackend'

EMAIL_HOST= "email-smtp.us-east-1.amazonaws.com"

EMAIL_PORT = 465

#EMAIL_PORT = 25

EMAIL_HOST_USER = "AKIAIDAJSTOZXJ4A3S5Q"

EMAIL_HOST_PASSWORD = "AsEbrGl82umzQoTR+EPgqWclt2eQ9FQyZfEkeSalmLWd"

#EMAIL_USE_TLS = True

