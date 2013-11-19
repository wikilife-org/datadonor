from os.path import abspath, dirname, basename, join


try:
    import social_auth
except ImportError:
    import sys
    sys.path.insert(0, '..')


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)

ADMINS = (
     ('Joaquin Quintas', 'joako84@gmail.com'),
)

import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/var/www/media/elearning/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media").replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ""

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
LANGUAGE_CODE = 'en-us'
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
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.linkedin.LinkedinOAuth2Backend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.evernote.EvernoteBackend',
    'physical.auth_backends.fitbit.FitbitBackend',
    'physical.auth_backends.runkeeper.RunkeeperBackend',
    'physical.auth_backends.fatsecret.FatsecretBackend',
    'genomics.auth_backends.twentythreeandme.TwentyThreeAndMeBackend',
    'social_auth.backends.contrib.dailymile.DailyMileBackend',
    'social_auth.backends.contrib.ihealth.IhealthBackend',
    'social_auth.backends.contrib.jawbone.JawboneBackend',
    'social_auth.backends.contrib.bodymedia.BodymediaBackend',
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
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/dashboard/"

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
    'pipeline.auth.social_aggretated_data',

    'pipeline.facebook.facebook_info',
    'pipeline.foursquare.foursquare_info',
    'pipeline.twitter.twitter_info',
    'pipeline.linkedin.linkedin_info',
    'pipeline.google.google_info',
    'pipeline.evernote.evernote_info',
    'pipeline.fitbit.fitbit_info',
    'pipeline.runkeeper.runkeeper_info',
    'pipeline.fatsecret.fatsecret_info',
    'pipeline.dailymile.dailymile_info',
    'pipeline.ihealth.ihealth_info',
    'pipeline.jawbone.jawbone_info',
    'pipeline.bodymedia.bodymedia_info',
    'pipeline.twentythreeandme.twentythreeandme_info',
    
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
    "runkeeper": 1, 
    "fitbit": 2, 
    "fatsecret": 3, 
    "facebook": 4, 
    "twitter": 5 
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

try:
    from conf_settings import *
except:
    pass


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
