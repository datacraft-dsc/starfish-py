"""

Test Surfer Model

- unit testing only on the surfer model.
You will still need to run the basic barge, since this needs a block chain network
for the ocean class to connect too.
"""

import pathlib
import logging
import json
from web3 import Web3


from starfish import Ocean
from starfish.models.surfer_model import SurferModel, SURFER_AGENT_ENDPOINT_NAME
from starfish import logger


from tests.helpers.surfer_mock import SurferMock

CONFIG_PARAMS = {'contracts_path': 'artifacts', 'keeper_url': 'http://localhost:8545' }
AGENT_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}


METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'

SURFER_URL= 'http://localhost:8080'

def _read_metadata():
    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

def test_register_asset():
    ocean = Ocean(CONFIG_PARAMS, log_level=logging.DEBUG)

    assert ocean
    assert ocean.accounts

    agent_account = ocean.get_account(AGENT_ACCOUNT)
    agent_account.unlock()

    agent_register = ocean.register_update_agent_service(SURFER_AGENT_ENDPOINT_NAME, SURFER_URL, agent_account )
    assert(agent_register)

    surferMock = SurferMock(SURFER_URL)

    model = SurferModel(ocean, agent_register[0], agent_register[1])
    SurferModel.set_http_client(surferMock)

    metadata = _read_metadata()
    result = model.register_asset(metadata['base'])
    assert(result)
    assert(result['asset_id'])
    assert(result['did'])
    assert(result['did'] == agent_register[0] + '/' + result['asset_id'])

