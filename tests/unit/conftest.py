from unittest.mock import Mock
import pytest
import secrets

from tests.unit.libs.unit_test_config import unitTestConfig
from tests.unit.libs.unit_test_network import UnitTestNetwork

@pytest.fixture(scope="module")
def config():
    return unitTestConfig

@pytest.fixture(scope="module")
def network(config):
    network = UnitTestNetwork(config.network_url)
    return network

@pytest.fixture(scope='module')
def accounts(config):
    accounts = []
    for acount_info in config.accounts:
        accounts.append(Account(account_info.as_dict))
    return accounts
