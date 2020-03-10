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


INTEGRATION_PATH = pathlib.Path.cwd() / 'tests' / 'integration'
CONFIG_FILE_PATH = INTEGRATION_PATH / 'config.ini'

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
    network = DNetwork()
    network.connect(config.network_url)
    return network


@pytest.fixture(scope="module")
def remote_agent(network, config):
    ddo_options = None
    services = Services(config.remote_agent_url, all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    options = {
        'username': config.remote_agent_username,
        'password': config.remote_agent_password,
    }
    return RemoteAgent(network, did=ddo.did, ddo=ddo, options=options)

@pytest.fixture(scope='module')
def accounts(config):
    result = [
        Account(config.account_1),
        Account(config.account_2)
    ]
    return result


@pytest.fixture(scope='module')
def invokable_list(config):

    url = f'{config.remote_agent_url}/api/v1/admin/import-demo?id=operations'
    username = config.remote_agent_username
    password = config.remote_agent_password
    response = requests.post(url, auth=(username, password), headers={'accept':'application/json'})
    result = response.json()
    return result.get('invokables')
