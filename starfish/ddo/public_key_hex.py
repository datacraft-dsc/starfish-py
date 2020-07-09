"""
    Public key HEX

    This is originally from
    https://github.com/oceanprotocol/squid-py/tree/b62b1bae303c499ca43f09dad1677001d9be840e/squid_py/ddo

"""

from .public_key_base import (
    PUBLIC_KEY_STORE_TYPE_HEX,
    PublicKeyBase
)

AUTHENTICATION_TYPE_HEX = 'HexVerificationKey'
PUBLIC_KEY_TYPE_HEX = 'PublicKeyHex'


class PublicKeyHex(PublicKeyBase):
    """Encode key value using Hex."""

    def __init__(self, key_id, **kwargs):
        PublicKeyBase.__init__(self, key_id, **kwargs)
        self._type = PUBLIC_KEY_TYPE_HEX
        self._store_type = PUBLIC_KEY_STORE_TYPE_HEX

    @property
    def authentication_type(self):
        """Return the type of authentication supported by this class."""
        return AUTHENTICATION_TYPE_HEX
