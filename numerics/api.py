import logging
import hashlib
from collections import namedtuple

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.utils.module_loading import import_string

from numerics import _ENDPOINTS

logger = logging.getLogger(__name__)

EndPoint = namedtuple('EndPoint', ['name',
                                   'code', 'cache_timeout', 'func',
                                   'args', 'kwargs'])

EndPointResponse = namedtuple('EndpointResponse', ['postfix', 'value'])

# returns an endpoint that is assigne to given name.
get_endpoint = _ENDPOINTS.get

_DEFAULT_SERIALIZER = 'numerics.serializers.BasicSerializer'
_CACHE = {}


def get_serializer():
    if 'serializer' in _CACHE:
        serializer = _CACHE['serializer']
    else:
        name = getattr(settings, 'NUMERICS_SERIALIZER_BACKEND',
                       _DEFAULT_SERIALIZER)
        serializer = import_string(name)()
        _CACHE['serializer'] = serializer
    return serializer


def register(name, func, args=None, kwargs=None, cache_timeout=60):

    if not args:
        args = []
    if not kwargs:
        kwargs = {}
    salt = settings.NUMERICS_SALT
    api_hash = hashlib.md5(str((name, salt)).encode()).hexdigest()
    if(name in _ENDPOINTS):
        logger.warn('Endpoint %s is already registered to numerics', name)
    else:
        _ENDPOINTS[api_hash] = EndPoint(name=name,
                                        code=api_hash,
                                        func=func,
                                        args=args,
                                        kwargs=kwargs,
                                        cache_timeout=cache_timeout)


# returns the endpoint for given cache.
# if there is no registered function, it returns None
get_endpoint_by_hash = _ENDPOINTS.get

def get_endpoint_url(user, endpoint):
    """Returns url string for given user and endpoint"""

    serializer = get_serializer()
    data = serializer.serialize(user, endpoint)
    return '{url}?endpoint={endpoint}'.format(
        url=reverse('numerics-index'),
        endpoint=urlquote(data))



# returns all endpoint list
def get_endpoint_urls(user):
    return {endpoint.name: get_endpoint_url(user, endpoint)
            for endpoint in _ENDPOINTS.values()}
