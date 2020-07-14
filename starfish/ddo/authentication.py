"""
    Authentication Class
    To handle embedded public keys
"""

import json
import re
from typing import Any
from .public_key_base import PublicKeyBase


class Authentication:
    """DDO Authentication"""

    def __init__(self, key_id: str, authentication_type: str) -> None:
        """ init an authentication based on it's key_id and authentication type"""
        self._public_key = None
        self._public_key_id = None
        if isinstance(key_id, PublicKeyBase):
            self._public_key = key_id
        else:
            self._public_key_id = key_id
        self._type = authentication_type

    def assign_did(self, did: str) -> None:
        """
        Assign a DID to the authentitacation, if the DID does not end with a `#.*`
        then add an automatic key value
        """
        if self._public_key_id:
            if re.match('^#.*', self._public_key_id):
                self._public_key_id = did + self._public_key_id
        if self._public_key:
            self._public_key.assign_did(did)

    @property
    def type(self) -> str:
        """get the authentication type"""
        return self._type

    @property
    def public_key_id(self) -> str:
        """ get the authentication key id used to validate this authentication"""
        if self._public_key_id:
            return self._public_key_id
        if self._public_key:
            return self._public_key.get_id()
        return None

    @property
    def public_key(self) -> str:
        """ get the authentication public key"""
        return self._public_key

    def as_text(self, is_pretty: bool = False) -> str:
        """ return the authentication as a JSON text"""
        values = {
            'type': self._type
        }
        if self._public_key:
            values['publicKey'] = self._public_key.as_text(is_pretty)
        elif self._public_key_id:
            values['publicKey'] = self._public_key_id

        if is_pretty:
            return json.dumps(values, indent=4, separators=(',', ': '))

        return json.dumps(values)

    @property
    def as_dictionary(self) -> Any:
        """ return the authentication as a dictionary"""
        values = {
            'type': self._type
        }
        if self._public_key:
            values['publicKey'] = self._public_key.as_dictionary()
        elif self._public_key_id:
            values['publicKey'] = self._public_key_id

        return values

    @property
    def is_valid(self) -> bool:
        """ return true if this authentication has valid structure"""
        return self.get_public_key_id() is not None and self._type is not None

    @property
    def is_public_key(self) -> bool:
        """ return true if this authentication has an embedded public key"""
        return self._public_key is not None

    def is_key_id(self, key_id: str) -> bool:
        """ return True if the `key_id` is the same as this key_id """
        if self.get_public_key_id() and self.get_public_key_id() == key_id:
            return True
        return False
