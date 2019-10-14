
from unittest.mock import Mock
import secrets

from tests.unit.libs.unit_test_account import UnitTestAccount

class UnitTestConfig():
    keeper_url = 'http://test-keeper-url:1234'
    contracts_path = 'test_artifacts_folder'
    gas_limit = 123456
    remote_agent_url = 'http://localhost:8080'
    accounts = {}
    def __init__(self):
        for index in range(0, 8):
            self.create_account(secrets.token_hex(32))

    def create_account(self, password):
        account = UnitTestAccount(password)
        self.accounts[len(self.accounts)] = account
        return account.address

unitTestConfig = UnitTestConfig()
