from unittest.mock import Mock
import pytest
import secrets
import logging
import pathlib
import requests
from web3 import Web3, HTTPProvider

from starfish import Network
from starfish.agent import RemoteAgent
from starfish.agent.services import Services
from starfish.account import Account

INTEGRATION_PATH = pathlib.Path.cwd() / 'tests' / 'integration'

logging.getLogger('web3').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)


@pytest.fixture(scope='module')
def network(config):
    network = Network(config['network']['url'])
    return network


@pytest.fixture(scope='module')
def remote_agent(config):
    ddo_options = None
    local_agent = config['agents']['local']
    services = Services(local_agent['url'], all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    authentication = {
        'username': local_agent['username'],
        'password': local_agent['password'],
    }
    return RemoteAgent(ddo, authentication)


@pytest.fixture(scope='module')
def accounts(config):
    result = []
    # load in the test accounts
    account_1 = config['accounts']['account1']
    account_2 = config['accounts']['account2']
    result = [
        Account(account_1['address'], account_1['password'], key_file=account_1['keyfile']),
        Account(account_2['address'], account_2['password'], key_file=account_2['keyfile']),
    ]
    return result


@pytest.fixture(scope='module')
def invokable_list(config):

    local_agent = config['agents']['local']

    url = f'{local_agent["url"]}/api/v1/admin/import-demo?id=operations'
    username = local_agent['username']
    password = local_agent['password']
    response = requests.post(url, auth=(username, password), headers={'accept':'application/json'})
    result = response.json()
    return result.get('invokables')
