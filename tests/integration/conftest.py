from unittest.mock import Mock
import pytest
import secrets
import logging
import pathlib
import requests
from web3 import Web3, HTTPProvider

from tests.integration.libs.integration_test_config import IntegrationTestConfig

from starfish import DNetwork
from starfish.agent import RemoteAgent
from starfish.agent.services import Services
from starfish.account import Account

RESOURCES_PATH = pathlib.Path.cwd() / 'tests' / 'resources'
INTEGRATION_PATH = pathlib.Path.cwd() / 'tests' / 'integration'
CONFIG_FILE_PATH = RESOURCES_PATH / 'config_local.conf'

logging.getLogger('web3').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)

@pytest.fixture(scope='module')
def intergation_config():
    integration_test_config = IntegrationTestConfig(CONFIG_FILE_PATH)
    return integration_test_config

@pytest.fixture(scope="module")
def config(intergation_config):
    return intergation_config

@pytest.fixture(scope="module")
def network(config):
    network = DNetwork(config.network_url)
    return network


@pytest.fixture(scope="module")
def remote_agent(network, config):
    ddo_options = None
    remote_agent = config.agent_list['remote']
    services = Services(remote_agent['url'], all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    authentication = {
        'username': remote_agent['username'],
        'password': remote_agent['password'],
    }
    return RemoteAgent(network, ddo, authentication)

@pytest.fixture(scope='module')
def accounts(config):
    result = [
        Account(config.account_1),
        Account(config.account_2)
    ]
    return result


@pytest.fixture(scope='module')
def invokable_list(config):

    remote_agent = config.agent_list['remote']

    url = f'{remote_agent["url"]}/api/v1/admin/import-demo?id=operations'
    username = remote_agent['username']
    password = remote_agent['password']
    response = requests.post(url, auth=(username, password), headers={'accept':'application/json'})
    result = response.json()
    return result.get('invokables')
