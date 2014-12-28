# Django settings for lscds_site project.

import os,sys 
<<<<<<< HEAD
DEBUG = True
TEMPLATE_DEBUG = DEBUG
=======
>>>>>>> e52b3bf76a7e1668ec1d7c47cc26da9b90940e0c
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
#print DATABASES
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH,'media')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'STATIC_URL')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1%83iw56w-4rlv&ryrguv5lz+3%^69ez1g(quz2(+e=8#gskmk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'zinnia.context_processors.version',
    "home.context_processors.latest",
    'django.core.context_processors.debug',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
IMAGESTORE_UPLOAD_TO = 'imagestore'
CKEDITOR_UPLOAD_PATH = "ckeditor/uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
ROOT_URLCONF = 'lscds_site.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lscds_site.wsgi.application'

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
TEMPLATE_PATH,
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # other stuff here,
    #'django_admin_bootstrapped',
    'django.contrib.admin',
    'django_comments',
    'tagging',
    'mptt',
    'zinnia','zinnia_ckeditor',

    'social.apps.django_app.default', 
    'lscdsUser',
    'home',
    'registration',
   # 'chance',
    'contact',
    'event','ckeditor',
     'photologue', 
     'imagekit',
     #'sortedm2m',
   #  'south',
    'home','sponsor',
    'institute',
    'crispy_forms','form_utils',
    #'imagestore',
    #'sorl.thumbnail',
    'tagging',
    #'autocomplete_light',
    'appengine_toolkit',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
APPENGINE_TOOLKIT = {
    # other settings here
 'APP_YAML': os.path.join(PROJECT_PATH, 'app.yaml'),
    'BUCKET_NAME': 'lscds-new-site.appspot.com',
}

IMAGEKIT_DEFAULT_FILE_STORAGE= 'appengine_toolkit.storage.GoogleCloudStorage'
DEFAULT_FILE_STORAGE = 'appengine_toolkit.storage.GoogleCloudStorage'
STATICFILE_STORAGE = 'appengine_toolkit.storage.GoogleCloudStorage'




IMAGESTORE_SHOW_USER =False
THUMBNAIL_PREFIX = 'gallery/'
THUMBNAIL_BACKEND = 'lscds_site.storage.SEOThumbnailBackend'
CACHES = {
        'default': {
            'BACKEND': 'appengine_toolkit.storage.GAEMemcachedCache',
            'TIMEOUT': 0,
        }
    }
AUTHENTICATION_BACKENDS = (
'social.backends.facebook.FacebookOAuth2',
'social.backends.google.GoogleOAuth2',
'social.backends.linkedin.LinkedinOAuth',
'social.backends.linkedin.LinkedinOAuth2',
 'social.backends.yahoo.YahooOAuth',
 'social.backends.yahoo.YahooOpenId',
'social.backends.twitter.TwitterOAuth',
 'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'lscdsUser.LscdsUser'


ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_SUBJECT_PREFIX = 'Your Registration With LSCDS'
SEND_ACTIVATION_EMAIL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
#SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
#    'https://www.googleapis.com/auth/drive',
#    'https://www.googleapis.com/auth/userinfo.profile'
#]
# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'example.app.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
   # 'social.pipeline.mail.mail_validation',
   # 'lscds_site.pipeline.require_email',
    'lscds_site.pipeline.social_extra_data',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'lscds_site.pipeline.user_details_complete'

    #'social.pipeline.debug.debug'
)


USER_FIELDS = ['email']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL=True
USERNAME_IS_FULL_EMAIL=True



SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=''

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=''


SOCIAL_AUTH_FACEBOOK_KEY =''
SOCIAL_AUTH_FACEBOOK_SECRET =''

SOCIAL_AUTH_YAHOO_OAUTH_SECRET = ''
SOCIAL_AUTH_YAHOO_OAUTH_KEY = ''


SOCIAL_AUTH_LINKEDIN_KEY=''
SOCIAL_AUTH_LINKEDIN_SECRET=''


SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress',]
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry')]

SOCIAL_AUTH_TWITTER_KEY=''
SOCIAL_AUTH_TWITTER_SECRET=''


SOCIAL_AUTH_LINKEDIN_KEY=''
SOCIAL_AUTH_LINKEDIN_SECRET=''


# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['first_name', 'last_name', 'email',
#                                         'username']
CRISPY_TEMPLATE_PACK = 'bootstrap3'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['first_name', 'last_name', 'email',
#                                         'username']

EMAIL_HOST          = "smtp.gmail.com" 
EMAIL_PORT          = 587
EMAIL_HOST_USER     = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS       = True # Yes for Gmail
DEFAULT_FROM_EMAIL  = "Life Science Carrier Development Services"
SERVER_EMAIL        = DEFAULT_FROM_EMAIL

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

try:
    from local_settings import *
except ImportError:
    pass
