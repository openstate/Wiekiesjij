from settings.default_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
#DEBUG_TOOLBAR = True
#Internal ip's used for debug toolbar and UserBasedExceptionMiddleware
#INTERNAL_IPS = ('127.0.0.1', '80.101.42.161')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'wiekiesjij_live',                      # Or path to database file if using sqlite3.
        'USER': 'wiekiesjij',                      # Not used with sqlite3.
        'PASSWORD': 'Vmxy8NjqiuXv9t',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


ADMINS = (
    ('WieKiesJij PS', 'webmaster@wiekiesjij.nl'),
)
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[WieKiesJij PS]'

#Change roots for user uploaded content and static files
MEDIA_ROOT = PROJECT_DIR('../../../media')
STATIC_ROOT = PROJECT_DIR('../static')

#Cache
CACHE_BACKEND = 'newcache://127.0.0.1:11211/?binary=true'
FLAVOR = 'live'

MIDDLEWARE_CLASSES += (
    'utils.middleware.PostLogMiddleware',
)
UTILS_POSTLOG_URLS = (
        r'^/backoffice/election/\d+/setup',
        r'^/backoffice/election/\d+/edit',
        r'^/backoffice/election/\d+/add_party',
        r'^/backoffice/party/\d+/setup',
        r'^/backoffice/party/\d+/edit',
        r'^/backoffice/party/\d+/add_candidate',
        r'^/backoffice/welcome/',
    )

#Disable menu on homepage and show static page on /
HOMEPAGE_PLACEHOLDER = False
GOOGLE_ANALYTICS_CODE = 'UA-1376555-5'

ELECTIONS_ELECTION_EVENT_ID = 3
ELECTIONS_ELECTION_INSTANCE_ID = 7

