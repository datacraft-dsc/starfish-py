
from unittest.mock import Mock
import secrets

from tests.unit.libs.unit_test_account import UnitTestAccount

class UnitTestConfig():
    network_url = 'http://test-keeper-url:1234'
    remote_agent_url = 'http://localhost:8080'
    accounts = []
    def __init__(self):
        for index in range(0, 8):
            account = self.create_account(secrets.token_hex(32))
            self.accounts.append(account)

    def create_account(self, password):
        account = UnitTestAccount(password)
        return account

unitTestConfig = UnitTestConfig()
