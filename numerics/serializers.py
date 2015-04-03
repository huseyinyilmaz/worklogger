"""Builtin Serilizers objects. for numerics mixin.

This Class Serializes current user and endpoint object to create
endpoint url.
"""

from django.utils.http import urlquote
from django.contrib.auth import get_user_model

from numerics.api import get_endpoint
from numerics.utils import get_fernet
from numerics.utils import encrypt
from numerics.utils import decrypt

from cryptography.fernet import InvalidToken


class SerializerException(Exception):
    pass


class BasicSerializer:

    """Basic serializer"""

    SEPARATOR = '|'

    def serialize(self, user, endpoint):

        return '{user_pk}{seperator}{endpoint_code}'.format(
            user_pk=user.pk,
            seperator=self.SEPARATOR,
            endpoint_code=endpoint.code)

    def deserialize(self, st):
        [user_pk, endpoint_code] = st.split('|')
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise SerializerException('User does not exist')
        endpoint = get_endpoint(endpoint_code)
        if not endpoint:
            raise SerializerException('Endpoint does not exist')
        return user, endpoint


class CryptoSerializer:

    """Serialize with cryptography."""

    def serialize(self, user, endpoint):
        return encrypt((user.pk, endpoint.code))

    def deserialize(self, st):
        try:
            (user_pk, endpoint_code) = decrypt(st)
        except InvalidToken:
            raise SerializerException('Invalid token. Cannot deserialize.')
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise SerializerException('User does not exist')
        endpoint = get_endpoint(endpoint_code)
        if not endpoint:
            raise SerializerException('Endpoint does not exist')
        return user, endpoint
