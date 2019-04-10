
import logging
from base64 import b64encode
from Cryptodome.PublicKey import RSA

from starfish.ddo.authentication import Authentication


from squid_py.ddo.ddo import DDO
from squid_py.ddo.public_key_base import PUBLIC_KEY_STORE_TYPE_PEM, PublicKeyBase
from squid_py.ddo.constants import KEY_PAIR_MODULUS_BIT
from squid_py.ddo.public_key_rsa import PublicKeyRSA


logger = logging.getLogger('ddo')

class StarfishDDO(DDO):

    def add_authentication(self, key_id, authentication_type=None):
        """
        Add a authentication public key id and type to the list of authentications.
        :param key_id: Key id, Authentication
        :param authentication_type: Authentication type, str
        :return: None
        """
        if isinstance(key_id, Authentication):
            # adding an authentication object
            authentication = key_id
        elif isinstance(key_id, PublicKeyBase):
            public_key = key_id
            # this is going to be a embedded public key
            authentication = Authentication(public_key, public_key.get_authentication_type())
        else:
            # with key_id as a string, we also need to provide the authentication type
            if authentication_type is None:
                raise ValueError
            authentication = Authentication(key_id, authentication_type)

        logger.debug(f'Adding authentication {authentication}')
        self._authentications.append(authentication)

    def add_signature(self, public_key_store_type=PUBLIC_KEY_STORE_TYPE_PEM, is_embedded=False):
        """
        Add signature.
        Add a signature with a public key and authentication entry for validating this DDO
        returns the private key as part of the private/public key pair.
        :param public_key_store_type: Public key store type, str
        :param is_embedded: bool
        :return Private key pem, str
        """

        key_pair = RSA.generate(KEY_PAIR_MODULUS_BIT, e=65537)
        public_key_raw = key_pair.publickey()
        private_key_pem = key_pair.exportKey("PEM")

        # find the current public key count
        next_index = self._get_public_key_count() + 1
        key_id = f'{self._did}#keys={next_index}'

        public_key = PublicKeyRSA(key_id, owner=key_id)

        public_key.set_encode_key_value(public_key_raw, public_key_store_type)

        if is_embedded:
            # also add the authentication key as embedded key with the authentication
            self.add_authentication(public_key)
        else:
            # add the public key to the DDO list of public keys
            self.add_public_key(None, public_key)

            # add the public key id and type for this key to the authentication
            self.add_authentication(public_key.get_id(), public_key.get_authentication_type())

        logger.debug('Adding signature to the ddo object.')
        return private_key_pem


    def add_public_key(self, did, public_key):
        """
        Add a public key object to the list of public keys.
        :param public_key: Public key, PublicKeyHex
        """
        if did == None:
            self._public_keys.append(public_key)
        else:
            logger.debug(f'Adding public key {public_key} to the did {did}')
            self._public_keys.append(
                PublicKeyBase(did, **{"owner": public_key, "type": "EthereumECDSAKey"}))


    def add_proof(self, authorisation_index, private_key=None, signature_text=None):
        """Add a proof to the DDO, based on the public_key id/index and signed with the private key
        add a static proof to the DDO, based on one of the public keys."""

        # find the key using an index, or key name
        if isinstance(authorisation_index, dict):
            self._proof = authorisation_index
            return

        if private_key is None:
            raise ValueError

        authentication = self._authentications[authorisation_index]
        if not authentication:
            raise IndexError

        if authentication.is_public_key():
            sign_key = authentication.get_public_key()
        else:
            sign_key = self.get_public_key(authentication.get_public_key_id())

        if sign_key is None:
            raise IndexError

        # get the signature text if not provided

        if signature_text is None:
            hash_text_list = self._hash_text_list()
            signature_text = "".join(hash_text_list)

        # just incase clear out the current static proof property
        self._proof = None

        signature = DDO.sign_text(signature_text, private_key, sign_key.get_type())

        self._proof = {
            'type': sign_key.get_type(),
            'created': DDO._get_timestamp(),
            'creator': sign_key.get_id(),
            'signatureValue': b64encode(signature).decode('utf-8'),
        }

    def _hash_text_list(self):
        """Return a list of all of the hash text."""
        hash_text = []
        if self._created:
            hash_text.append(self._created)

        if self._public_keys:
            for public_key in self._public_keys:
                if public_key.get_type():
                    hash_text.append(public_key.get_type())
                if public_key.get_value():
                    hash_text.append(public_key.get_value())

        if self._authentications:
            for authentication in self._authentications:
                if authentication.is_public_key():
                    public_key = authentication.get_public_key()
                    if public_key.get_type():
                        hash_text.append(public_key.get_type())
                    if public_key.get_value():
                        hash_text.append(public_key.get_value())

        if self._services:
            for service in self._services:
                hash_text.append(service.type)
                hash_text.extend(service.endpoints)

        # if no data can be found to hash then raise an error
        if not hash_text:
            raise ValueError
        return hash_text
