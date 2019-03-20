from unittest.mock import Mock
import pytest
import secrets

from starfish import Ocean




class TestConfig():
    keeper_url = 'http://test-keeper-url:1234'
    contracts_path = 'test_artifacts_folder'
    gas_limit = 123456
    accounts = {}
    def __init__(self):
        for index in range(0, 8):
            self.accounts[index] = (secrets.token_hex(32), 'test_password')



testConfig = TestConfig()


@pytest.fixture(scope="module")
def ocean():
    result = Ocean(keeper_url=testConfig.keeper_url,
            contracts_path=testConfig.contracts_path,
            gas_limit=testConfig.gas_limit
    )
    return result
