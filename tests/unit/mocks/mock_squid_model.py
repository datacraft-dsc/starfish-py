from unittest.mock import Mock
import pytest
import secrets

from starfish.ddo.starfish_ddo import StarfishDDO

from squid_py.did import (
    id_to_did,
    did_to_id_bytes,
)

from tests.unit.libs.unit_test_config import unitTestConfig


class MockSquidModel():
    def __init__(self, ocean, options=None):
        """init a standard ocean object"""
        self._ocean = ocean

    def get_account(self, address, password=None):
        if address:
            for index in unitTestConfig.accounts:
                test_account = unitTestConfig.accounts[index]
                if address.lower() == test_account.test_address.lower():
                    account = Mock()
                    account.address = address
                    if password:
                        account.password = password
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

    def get_account_balance(self, account):
        for index in unitTestConfig.accounts:
            test_account = unitTestConfig.accounts[index]
            if account.address.lower() == test_account.test_address.lower():
                balance = Mock()
                balance.eth = test_account.test_ether
                balance.ocn = test_account.test_tokens
                return balance
        return 0

    def create_account(self, password = None):
        address = unitTestConfig.create_account(password)
        return self.get_account(address, password)

    def request_tokens(self, account, value):
        found_account = self.get_account(account.address)
        if found_account.address == account.address:
            return value
        return 0

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
