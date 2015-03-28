from os.path import expanduser
from worklogger.base import *  # noqa

INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

###############################
# DJANGO DEBUG TOOLBAR CONFIG #
###############################

# See:
# https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See:
# https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
    }

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )


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
            'level': 'WARNING',
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
if 'raven' in secretkeys:
    #  RAVEN_CONVIGURATION

    RAVEN_CONFIG = {
        'dsn': secretkeys['raven']['dns']
    }

    INSTALLED_APPS += ('raven.contrib.django.raven_compat', )

    # Add root sentry logger to root handler
    LOGGING['handlers']['sentry'] = {
        'level': 'INFO',
        'class':
        'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }

    LOGGING['root']['handlers'].append('sentry')

    LOGGING['loggers']['raven'] = {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
        'propagate': False,
    }
