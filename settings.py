import os
PROJECT_DIR = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

_ = lambda a: a

DEBUG = True
DEBUG_TOOLBAR = DEBUG
TEMPLATE_DEBUG = DEBUG
TEMPLATE_COMMENTS = True
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = PROJECT_DIR('dev.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_DIR('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/static/admin/'

#Static files settings
STATIC_ROOT = PROJECT_DIR('media/static')
STATIC_URL = '/media/static/'

#Directory for temporary files
TMP_ROOT = PROJECT_DIR('tmp')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1-r)jw8q4x*ci!j9(mchfn&^a3ez&9p5ab6#@6s++t!t%sei=t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'utils.middleware.PermissionDeniedMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'staticfiles.context_processors.static_url',
    'elections.context_processors.election_event',
)

TEMPLATE_DIRS = (
    PROJECT_DIR('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.comments',
    
    #general utils
    'south',
    'django_extensions',
    'staticfiles',
    'sorl.thumbnail',
    
    'elections',
    'political_profiles',
    'authorized_comments',
    'questions',
    'utils',

    'invitations',
    'backoffice',
    'frontoffice',
    'registration',

    'opensocial',
)

COMMENTS_APP = 'authorized_comments'

# Email settings
EMAIL_HOST = 'smtp.xs4all.nl'
EMAIL_HOST_USER = 'accepte'
EMAIL_HOST_PASSWORD = '9712hv'
EMAIL_USE_TLS = True
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'info@wiekiesjij.nl'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

#login logout related
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/redirect/'
UTILS_PERMISSION_DENIED_URL = '/backoffice/permission_denied/'

ACCOUNT_ACTIVATION_DAYS = 7

AUTHENTICATION_BACKENDS = (
    'utils.auth_backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

try:
    from local_settings import *
except ImportError:
    pass


#Settings
COMMON_PARTIES =  (('CDA', _('CDA')),
                   ('PvdA', _('PvdA')),
                   ('SP', _('SP')),
                   ('VVD', _('VVD')),
                   ('PVV', _('PVV')),
                   ('GL', _('GL')),
                   ('CU', _('CU')),
                   ('D66', _('D66')),
                   ('PvdD', _('PvdD')),
                   ('SGP', _('SGP')),
                   ('OSF', _('OSF')),)
ELECTIONS_CONTACT_LIMITATION = {'contactprofile__isnull': False}
ELECTIONS_CHANCERY_LIMITATION = {'chanceryprofile__isnull': False}
ELECTIONS_POLITICIAN_LIMITATION = {'politicianprofile__isnull': False}
ELECTIONS_PROFILE_APP = 'political_profiles'

ELECTIONS_ELECTION_EVENT_ID = 1



# Wizard specific settings
WIZARD_TIMEOUT = False
WIZARD_KEEP_DATA = False
WIZARD_UPLOAD_TEMP_DIR = PROJECT_DIR('tmp')


if DEBUG and DEBUG_TOOLBAR:

    #debug_toolbar
    MIDDLEWARE_CLASSES += (
       'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    
    INTERNAL_IPS = ('127.0.0.1',)
    
    INSTALLED_APPS += (
       'debug_toolbar',
    )
    
    DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
    }
        
    #end debug_toolbar

if NOT DEBUG:
    MIDDLEWARE_CLASSES += (
        'utils.middleware.PostLogMiddleware',
    )
    UTILS_POSTLOG_URLS = (
        r'^/backoffice/election/\d+/setup',
        r'^/backoffice/party/\d+/setup',
        r'^/backoffice/welcome/\d+',
    )
    