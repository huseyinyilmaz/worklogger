"""
Django settings for worklogger project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import exists
from os.path import expanduser

import configparser


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

secrets_file = os.path.join(BASE_DIR, 'worklogger', 'secrets.ini')
assert exists(secrets_file), ('You need secrets.ini file '
                              'inside worklogger directory')

# disable interpolation
# We have % character on ini file
secretkeys = configparser.ConfigParser(interpolation=None)
secretkeys.read(secrets_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = secretkeys['django']['secret-key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'registration',
    'floppyforms',
    'djangonumerics',
    )

LOCAL_APPS = (
    'accounts',
    'core',
    'logs',
    )

DEV_APPS = (
    'django_extensions',
    )

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + DEV_APPS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'worklogger.urls'

WSGI_APPLICATION = 'worklogger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'logs.context_processors.running_logs',
)
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/accounts/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

# REGISTRATION

# REGISTRATION_FORM = 'registration.forms.RegistrationFormUniqueEmail'
ACCOUNT_ACTIVATION_DAYS = 30
REGISTRATION_OPEN = True

# EMAIL BACKEND
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'Huseyin Yilmaz <huseyin@yilmazhuseyin.com>'

# EMAIL_CONFIGURATION
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secretkeys['email']['email']
EMAIL_HOST_PASSWORD = secretkeys['email']['password']
EMAIL_PORT = 587

# NUMERICS SETTINGS
DJANGO_NUMERICS_ENABLED = True
DJANGO_NUMERICS_SERIALIZER_BACKEND = \
    'djangonumerics.serializers.CryptoSerializer'
DJANGO_NUMERICS_SECRET_KEY = secretkeys['numerics']['secret-key']
DJANGO_NUMERICS_SALT = secretkeys['numerics']['salt']


#####################
# LOG CONFIGURATION #
#####################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': expanduser('~/logs/worklogger.log'),
        },


    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'propagate': False,
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    }
}


# if raven is provided add it to handlers
if 'raven' in secretkeys and not DEBUG:
    #  RAVEN_CONVIGURATION

    RAVEN_CONFIG = {
        'dsn': secretkeys['raven']['dns']
    }

    INSTALLED_APPS += ('raven.contrib.django.raven_compat', )

    # Add root sentry logger to root handler
    LOGGING['handlers']['sentry'] = {
        'level': 'WARNING',
        'class':
        'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }

    LOGGING['root']['handlers'].append('sentry')

    LOGGING['loggers']['raven'] = {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
        'propagate': False,
    }
