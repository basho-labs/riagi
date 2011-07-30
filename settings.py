import os.path
import riak
import django_riak
import pwd
import os

# Django settings for riagi project.

if pwd.getpwuid(os.getuid())[0] == "dotcloud":
    RIAK_HOST = "riak01.riagi.com"
    RIAK_PORT = "8098"
    DEBUG = False
else:
    RIAK_HOST = "127.0.0.1"
    RIAK_PORT = "8098"
    DEBUG = True

TEMPLATE_DEBUG = DEBUG
RIAK_PROTOCOL = "http"
RIAK_USERS_BUCKET = "riagi-users"
RIAK_IMAGE_BUCKET = "riagi-images"
RIAK_THUMBS_BUCKET = "riagi-thumbs"
RIAK_METADATA_BUCKET = "riagi-image-metadata"
FILE_UPLOAD_MAX_MEMORY_SIZE = 0

RIAK_TRANSPORT_CLASS = riak.RiakHttpTransport
RIAK_BUCKET = 'django-riak-sessions'
SESSION_ENGINE = "django_riak"
APPEND_SLASH = False
TIME_ZONE = 'Europe/London' 
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

MEDIA_URL = ''
STATIC_URL = '/static/'
STATIC_ROOT = ''
MEDIA_ROOT = ''

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = ')^)dn9@fe=7=7lurgj#$r9)h$1y9h*zc@kzdur46nd6l@qe%)!'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'images',
    'users'
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.debug",
"django.core.context_processors.i18n", "django.core.context_processors.media",
'django.core.context_processors.request',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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
