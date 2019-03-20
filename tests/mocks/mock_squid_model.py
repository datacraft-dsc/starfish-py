from unittest.mock import Mock
import pytest
import secrets

from squid_py.ddo.ddo import DDO
from squid_py.did import (
    id_to_did,
    did_to_id_bytes,
)

from tests.unit.test_config import testConfig


class MockSquidModel():
    def __init__(self, ocean, options=None):
        """init a standard ocean object"""
        self._ocean = ocean

    def get_account(self, address, password=None):
        account = Mock()
        account.address = address
        account.password = password
        return account

    def register_agent(self, service_name, endpoint_url, account, did=None):
        # if no did then we need to create a new one
        did = id_to_did(secrets.token_hex(32))

        # create a new DDO
        ddo = DDO(did)
        # add a signature
        private_key_pem = ddo.add_signature()
        # add the service endpoint with the meta data
        ddo.add_service(service_name, endpoint_url)
        # add the static proof
        ddo.add_proof(0, private_key_pem)
        # if self.register_ddo(did, ddo, account._squid_account):
        return [did, ddo, private_key_pem]

    @property
    def accounts(self):
        result = []
        for index in range(0, len(testConfig.accounts)):
            mock_account = Mock()
            mock_account.address = testConfig.accounts[index][0]
            mock_account.password = testConfig.accounts[index][1]
            result.append(mock_account)

        return result
