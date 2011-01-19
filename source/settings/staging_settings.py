from settings.default_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'wiekiesjij_stag',                      # Or path to database file if using sqlite3.
        'USER': 'wiekiesjij',                      # Not used with sqlite3.
        'PASSWORD': 'Vmxy8NjqiuXv9t',                  # Not used with sqlite3.
        'HOST': '192.168.151.113',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


ADMINS = (
    ('WieKiesJij PS', 'exceptions@getlogic.nl'),
)
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[WieKiesJij PS Staging]'

#Change roots for user uploaded content and static files
MEDIA_ROOT = PROJECT_DIR('../../../media')
STATIC_ROOT = PROJECT_DIR('../static')

#Cache
#CACHE_BACKEND = 'newcache://127.0.0.1:11211/?binary=true'
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
HOMEPAGE_PLACEHOLDER = True