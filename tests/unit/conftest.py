from unittest.mock import Mock
import pytest
import secrets

from tests.unit.libs.unit_test_config import unitTestConfig

@pytest.fixture(scope="module")
def config():
    return unitTestConfig

"""
@pytest.fixture(scope="module")
def ethereum_network(config):
    network = UnitTestNetwork(config.ethereum.network_url)
    return network

@pytest.fixture(scope='module')
def ethereum_accounts(config):
    accounts = []
    for acount_info in config.ethereum.accounts:
        accounts.append(Account(account_info.as_dict))
    return accounts
"""
