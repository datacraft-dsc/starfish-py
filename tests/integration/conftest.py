from unittest.mock import Mock
import pytest
import secrets
import logging
import pathlib
import requests
from web3 import Web3, HTTPProvider

from starfish.agent import RemoteAgent
from starfish.network.ddo import DDO

"""
from starfish.network.ethereum import (
    EthereumAccount,
    EthereumNetwork
)
"""

from starfish.network.convex import (
    ConvexAccount,
    ConvexNetwork
)

from tests.integration.network.convex.helpers import auto_topup_account


INTEGRATION_PATH = pathlib.Path.cwd() / 'tests' / 'integration'

logging.getLogger('web3').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)


@pytest.fixture(scope='module')
def convex_network(config):
    network = ConvexNetwork(config['convex']['network']['url'])
    return network


@pytest.fixture(scope='module')
def remote_agent_surfer(config):
    ddo_options = None
    local_agent = config['agents']['surfer']
    ddo = DDO.create(local_agent['url'], [
        'meta',
        'storage',
        'invoke',
        'market',
        'trust',
        'auth'
    ])
    authentication = {
        'username': local_agent['username'],
        'password': local_agent['password'],
    }
    return RemoteAgent(ddo, authentication)

@pytest.fixture(scope='module')
def remote_agent_invokable(config):
    ddo_options = None
    local_agent = config['agents']['invokable']
    ddo = DDO.create(local_agent['url'])
    authentication = {
        'username': local_agent['username'],
        'password': local_agent['password'],
    }
    return RemoteAgent(ddo, authentication)


@pytest.fixture(scope='module')
def convex_accounts(config, convex_network):
    result = []
    # load in the test accounts
    account_1 = config['convex']['accounts']['account1']
    import_account = ConvexAccount.import_from_file(account_1['keyfile'], account_1['password'])

    accounts = [
        convex_network.setup_account(account_1['name'], import_account),
        convex_network.create_account(import_account),
    ]
    auto_topup_account(convex_network, accounts)
    return accounts



@pytest.fixture(scope='module')
def invokable_list(config):

    local_agent = config['agents']['surfer']

    url = f'{local_agent["url"]}/api/v1/admin/import-demo?id=operations'
    username = local_agent['username']
    password = local_agent['password']
    response = requests.post(url, auth=(username, password), headers={'accept':'application/json'})
    result = response.json()
    return result.get('invokables')
