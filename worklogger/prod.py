from worklogger.base import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS.extend(['www.yilmazhuseyin.com', # noqa
                      'worklogger.yilmazhuseyin.com'])

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'KEY_PREFIX': 'worklogger',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#         'LOCATION': '127.0.0.1:11211',
#         'KEY_PREFIX': 'worklogger',
#     }
# }
