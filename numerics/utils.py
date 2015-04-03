import json
from django.conf import settings

from cryptography.fernet import Fernet

_FERNET_ENCODING = 'ascii'
_FERNET_KEY = 'fernet'

_CACHE = {}


def get_fernet():
    """Returns fernet object. Object is encoded on module level.
    """

    if _FERNET_KEY not in _CACHE:
        key = bytes(settings.NUMERICS_SECRET_KEY, _FERNET_ENCODING)
        _CACHE[_FERNET_KEY] = Fernet(key)

    return _CACHE[_FERNET_KEY]


def encrypt(data):
    data_json = json.dumps(data)
    data_bytes = bytes(data_json, _FERNET_ENCODING)
    return get_fernet().encrypt(data_bytes).decode('utf-8')


def decrypt(data):
    # make sure that data is str or bytes string
    if isinstance(data, str):
        data = bytes(data, _FERNET_ENCODING)
    elif isinstance(data, bytes):
        # it is already in right format
        pass
    else:
        ValueError('data should have type of either str or bytes')

    decrypted_data = get_fernet().decrypt(data).decode('utf-8')
    return json.loads(decrypted_data)
