from unittest.mock import Mock
import pytest
import secrets
import logging
import pathlib
import requests
from web3 import Web3, HTTPProvider

from tests.integration.libs.integration_test_config import IntegrationTestConfig

from starfish import Ocean
from starfish.agent import (
    RemoteAgent,
    SquidAgent,
)

from starfish.agent.services import Services
from starfish.account import StarfishAccount


INTEGRATION_PATH = pathlib.Path.cwd() / 'tests' / 'integration'
CONFIG_FILE_PATH = INTEGRATION_PATH / 'config.ini'

logging.getLogger('web3').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)

@pytest.fixture(scope='module')
def intergation_config():
    integration_test_config = IntegrationTestConfig(CONFIG_FILE_PATH)
    return integration_test_config

@pytest.fixture(scope="module")
def ocean(intergation_config):
    ocean = Ocean(
        keeper_url=intergation_config.keeper_url,
        contracts_path=intergation_config.contracts_path,
        gas_limit=intergation_config.gas_limit,
        log_level=logging.WARNING
    )

    return ocean

@pytest.fixture(scope='module')
def w3(intergation_config):
    return Web3(HTTPProvider(intergation_config.keeper_url))

@pytest.fixture(scope="module")
def config(intergation_config):
    return intergation_config

@pytest.fixture(scope="module")
def remote_agent(ocean, intergation_config):
    ddo_options = None
    services = Services(intergation_config.remote_agent_url, all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    options = {
        'username': intergation_config.remote_agent_username,
        'password': intergation_config.remote_agent_password,
    }
    return RemoteAgent(ocean, did=ddo.did, ddo=ddo, options=options)

@pytest.fixture(scope="module")
def squid_agent(ocean, intergation_config):
    return SquidAgent(ocean, intergation_config.squid_config)

@pytest.fixture(scope='module')
def publisher_account(ocean, config):
    return ocean.load_account(config.publisher_account['address'], config.publisher_account['password'], config.publisher_account['keyfile'])


@pytest.fixture(scope='module')
def purchaser_account(ocean, config):
    return ocean.load_account(config.purchaser_account['address'], config.purchaser_account['password'], config.purchaser_account['keyfile'])

@pytest.fixture(scope='module')
def starfish_accounts(config):
    result = {
        'publisher': StarfishAccount(config.publisher_account),
        'purchaser': StarfishAccount(config.purchaser_account)
    }
    return result

@pytest.fixture(scope='module')
def agent_account(ocean, config):
    return ocean.load_account(config.agent_account['address'], config.agent_account['password'], config.agent_account['keyfile'])

@pytest.fixture(scope='module')
def invokable_list(config):

    url = f'{config.remote_agent_url}/api/v1/admin/import-demo?id=operations'
    username = config.remote_agent_username
    password = config.remote_agent_password
    response = requests.post(url, auth=(username, password), headers={'accept':'application/json'})
    result = response.json()
    return result.get('invokables')
