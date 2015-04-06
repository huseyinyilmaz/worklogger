from worklogger.base import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS.extend(['www.yilmazhuseyin.com',
                      'worklogger.yilmazhuseyin.com'])

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'worklogger',
    }
}
