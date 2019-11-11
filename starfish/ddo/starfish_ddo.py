
import logging
import json
from base64 import b64encode
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5

from starfish.ddo.authentication import Authentication


from ocean_utils.ddo.ddo import DDO

from ocean_utils.ddo.public_key_base import PUBLIC_KEY_STORE_TYPE_PEM, PublicKeyBase
from ocean_utils.ddo.constants import KEY_PAIR_MODULUS_BIT, DID_DDO_CONTEXT_URL, PROOF_TYPE
from ocean_utils.ddo.public_key_rsa import PublicKeyRSA, PUBLIC_KEY_TYPE_RSA
from ocean_utils.ddo.service import Service


logger = logging.getLogger('starfish.ddo')

class StarfishDDO(DDO):

    def set_service_endpoint(self, service_type, value):
        """

        Set the default service endpoint with a new value

        :param service_type: Type of service to set
        :param value: value to set as the new value

        """
        service = self.get_service(service_type)
        if service:
            service._service_endpoint = value

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
        if did is None:
            self._public_keys.append(public_key)
        else:
            logger.debug(f'Adding public key {public_key} to the did {did}')
            self._public_keys.append(
                PublicKeyBase(did, **{"owner": public_key, "type": "EthereumECDSAKey"}))

    def add_proof_keeper(self, text, publisher_account, keeper):
        """Add a proof to the DDO, based on the public_key id/index and signed with the private key
        add a static proof to the DDO, based on one of the public keys."""

        # just incase clear out the current static proof property
        self._proof = None
        self._proof = {
            'type': PROOF_TYPE,
            'created': DDO._get_timestamp(),
            'creator': publisher_account.address,
            'signatureValue': keeper.sign_hash(text, publisher_account),
        }

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

        signature = StarfishDDO.sign_text(signature_text, private_key, sign_key.get_type())

        self._proof = {
            'type': sign_key.get_type(),
            'created': DDO._get_timestamp(),
            'creator': sign_key.get_id(),
            'signatureValue': b64encode(signature).decode('utf-8'),
        }

    def as_dictionary(self, is_proof=True):
        """
        Return the DDO as a JSON dict.
        :param if is_proof: if False then do not include the 'proof' element.
        :return: dict
        """
        if self._created is None:
            self._created = DDO._get_timestamp()

        data = {
            '@context': DID_DDO_CONTEXT_URL,
            'id': self._did,
            'created': self._created,
        }
        if self._public_keys:
            values = []
            for public_key in self._public_keys:
                values.append(public_key.as_dictionary())
            data['publicKey'] = values
        if self._authentications:
            values = []
            for authentication in self._authentications:
                values.append(authentication.as_dictionary())
            data['authentication'] = values
        if self._services:
            values = []
            for service in self._services:
                values.append(service.as_dictionary())
            data['service'] = values
        if self._proof and is_proof:
            data['proof'] = self._proof

        return data

    def _read_dict(self, dictionary):
        """Import a JSON dict into this DDO."""
        values = dictionary
        self._did = values['id']
        self._created = values.get('created', None)
        if 'publicKey' in values:
            self._public_keys = []
            for value in values['publicKey']:
                if isinstance(value, str):
                    value = json.loads(value)
                self._public_keys.append(DDO.create_public_key_from_json(value))
        if 'authentication' in values:
            self._authentications = []
            for value in values['authentication']:
                if isinstance(value, str):
                    value = json.loads(value)
                self._authentications.append(StarfishDDO.create_authentication_from_json(value))
        if 'service' in values:
            self._services = []
            for value in values['service']:
                if isinstance(value, str):
                    value = json.loads(value)
                service = Service.from_json(value)
                service.set_did(self._did)
                self._services.append(service)
        if 'proof' in values:
            self._proof = values['proof']

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
                hash_text.extend(service.endpoints[0])

        # if no data can be found to hash then raise an error
        if not hash_text:
            raise ValueError
        return hash_text

    @staticmethod
    def create_authentication_from_json(values):
        """Create authentitaciton object from a JSON string."""
        key_id = values.get('publicKey')
        authentication_type = values.get('type')
        if not key_id:
            raise ValueError(
                f'Invalid authentication definition, "publicKey" is missing: {values}')
        if isinstance(key_id, dict):
            public_key = DDO.create_public_key_from_json(key_id)
            authentication = Authentication(public_key, public_key.get_authentication_type())
        else:
            authentication = Authentication(key_id, authentication_type)

        return authentication

    @staticmethod
    def sign_text(text, private_key, sign_type=PUBLIC_KEY_TYPE_RSA):
        """Sign some text using the private key provided."""
        if sign_type == PUBLIC_KEY_TYPE_RSA:
            signer = PKCS1_v1_5.new(RSA.import_key(private_key))
            text_hash = SHA256.new(text.encode('utf-8'))
            signed_text = signer.sign(text_hash)
            return signed_text

        raise NotImplementedError
