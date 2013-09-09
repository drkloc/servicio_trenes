import os
import sys
sys.path.append(os.getcwd())
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Teofilo Sibileau', 'teo.sibileau@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.dummy'
    }
}


TIME_ZONE = 'America/Argentina/Buenos_Aires'

LANGUAGE_CODE = 'es-AR'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3g1pv(e9kri0$mk&$i!xs9u5piaz&bejdnzdf$&wjaf&w0ir#2'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'servicetrenes.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'djcelery',
    'core',
    'lineas',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'trenes_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(
                SITE_ROOT,
                'log',
                'trenes.log'
            ),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'trenes': {
            'handlers': ['trenes_logfile'],
            'level': 'DEBUG',
        },
    }
}
