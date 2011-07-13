import os.path
import django_riak
# Django settings for riagi project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

RIAK_HOST = "127.0.0.1"
RIAK_PORT = "8098"
RIAK_PROTOCOL = "http"
RIAK_USERS_BUCKET = "riagi-users"
RIAK_IMAGE_BUCKET = "riagi-images"
RIAK_META_DATA_BUCKET = "riagi-image-metadata"

SESSION_ENGINE="django_riak"

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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
    'images'
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

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
