from unittest.mock import Mock
import pytest
import secrets
import json
import re
from web3 import Web3

from starfish.ddo.starfish_ddo import StarfishDDO
from starfish.middleware.squid_agent_adapter import SquidAgentAdapterPurchaseError

from ocean_utils.did import (
    did_to_id,
    id_to_did,
    did_to_id_bytes,
)
from ocean_utils.agreements.service_types import ServiceTypes
from squid_py.ocean.keeper import SquidKeeper
from plecos import is_valid_dict_local, validate_dict_local


from tests.unit.libs.unit_test_config import unitTestConfig

TEST_SERVICE_NAME = 'service_data'

class MockKeeper():
    def sign_hash(self, text, publisher_account):
        return Web3.sha3(text=text + publisher_account.address)


class MockSquidAgentAdapter():
    def __init__(self, ocean, options=None):
        """init a standard ocean object"""
        self._ocean = ocean
        self._options = options
        self._metadata = {}
        self._ddo_list = {}
        self._purchase_assets={}
        self._account_list = {}

    def get_account(self, address, password=None, keyfile=None):
        if address:
            for index in unitTestConfig.accounts:
                test_account = unitTestConfig.accounts[index]
                if address.lower() == test_account.test_address.lower():
                    account = Mock()
                    account.address = address
                    if password:
                        account.password = password
                    if keyfile:
                        account.keyfile = keyfile
                    self._account_list[address] = account
                    return account
        return None

    def register_agent(self, service_name, endpoint_url, account, did=None):
        # if no did then we need to create a new one
        did = id_to_did(secrets.token_hex(32))

        # create a new DDO
        ddo = StarfishDDO(did)
        # add a signature
        private_key_pem = ddo.add_signature()
        # add the service endpoint with the meta data
        ddo.add_service(service_name, endpoint_url)
        # add the static proof
        ddo.add_proof(0, private_key_pem)
        # if self.register_ddo(did, ddo, account._squid_account):
        return [did, ddo, private_key_pem]

    def validate_metadata(self, metadata):
        """

        Validate the metadata with plesto

        :param dict metadata: metadata to validate
        :return: True if the metadata is valid
        :type: boolean

        """
        if is_valid_dict_local(metadata):
            return True
        else:
            validator = validate_dict_local(metadata)

        return False

    def register_ddo(self, did, ddo, account):
        self._ddo_list[did] = ddo
        return secrets.token_hex(32)

    def resolve_did(self, did):
        return self._ddo_list[did]

    def register_asset(self, metadata, account ):
        did = id_to_did(secrets.token_hex(32))
        self._metadata[did] = metadata

        # create a new DDO
        ddo = StarfishDDO(did)
        # add a signature
        private_key_pem = ddo.add_signature()
        # add the service endpoint with the meta data
        assert(self._options)
        assert('aquarius_url' in self._options)
        ddo.add_service(TEST_SERVICE_NAME, self._options['aquarius_url'])
        ddo.add_service(ServiceTypes.METADATA, '', {'metadata': metadata})
        # add the static proof

        mockKeeper = MockKeeper()

        if not 'checksum' in metadata['base']:
            metadata['base']['checksum'] = did

        ddo.add_proof_keeper(metadata['base']['checksum'], account, mockKeeper)
        # if self.register_ddo(did, ddo, account._squid_account):
        self._ddo_list[did] = ddo
        return ddo

    def search_assets(self, text, sort=None, offset=100, page=0):
        result = []
        for ddo in self._ddo_list.values():
            metadata_text = json.dumps(ddo.metadata)
            if re.search(text, metadata_text):
                result.append(ddo)

        return result

    def read_asset(self, did):
        return self._ddo_list[did]

    def purchase_asset(self, ddo, account):
        service = ddo.get_service(TEST_SERVICE_NAME)
        assert(service)
        service_dict = service.as_dictionary()
        assert(service_dict['serviceEndpoint'] == self.options['aquarius_url'])
        service_agreement_id = secrets.token_hex(32)
        self._purchase_assets[service_agreement_id] = ddo.did
        return service_agreement_id

    def purchase_wait_for_completion(self, asset, account, purchase_id, timeoutSeconds):
        if purchase_id:
            return True
        raise SquidAgentAdapterPurchaseError('test squid agent adapter purchase wait error')

    def consume_asset(self, ddo, account, service_agreement_id):
        service = ddo.get_service(TEST_SERVICE_NAME)
        assert(service)
        service_dict = service.as_dictionary()
        assert(service_dict['serviceEndpoint'] == self.options['aquarius_url'])
        assert(service_agreement_id in self._purchase_assets)
        did = self._purchase_assets[service_agreement_id]
        if not did in self._metadata:
            return False
        return self._metadata[did]['base']['files']


    def is_access_granted_for_asset(self, did, account, service_agreement_id=None):
        if did in self._metadata and service_agreement_id in self._purchase_assets:
            return True
        return False

    def get_account_balance(self, account):
        for index in unitTestConfig.accounts:
            test_account = unitTestConfig.accounts[index]
            if account.address.lower() == test_account.test_address.lower():
                balance = Mock()
                balance.eth = Web3.toWei(test_account.test_ether, 'ether')
                balance.ocn = Web3.toWei(test_account.test_tokens, 'ether')
                return balance
        return 0

    @property
    def accounts(self):
        """
        Not used at the moment
        """
        return self._account_list

    def request_tokens(self, value, account):
        found_account = self.get_account(account.address, account.password, account.keyfile)
        if found_account.address == account.address:
            return value
        return 0

    """
    @property
    def accounts(self):
        result = []
        for index in unitTestConfig.accounts:
            test_account = unitTestConfig.accounts[index]
            account = Mock()
            account.address = test_account.test_address,
            account.password = test_account.test_password
            result.append(account)

        return result
    """

    @property
    def options(self):
        return self._options
