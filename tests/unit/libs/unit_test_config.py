
from unittest.mock import Mock
import secrets

from tests.unit.libs.unit_test_account import UnitTestAccount

class UnitTestConfig():
    keeper_url = 'http://test-keeper-url:1234'
    contracts_path = 'test_artifacts_folder'
    gas_limit = 123456
    accounts = {}
    def __init__(self):
        for index in range(0, 8):
            account = UnitTestAccount()
            self.accounts[index] = account


unitTestConfig = UnitTestConfig()
