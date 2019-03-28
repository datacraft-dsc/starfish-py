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
from starfish.models.surfer_model import SurferModel
from starfish.agent import SurferAgent
from starfish import logger


from tests.integration.mocks.surfer_mock import SurferMock


def test_register_asset(ocean, metadata, config):

    agent_account = ocean.get_account(config.agent_account)
    agent_account.unlock()

    agent_register = ocean.register_update_agent_service(SurferAgent.endPointName, config.surfer_url, agent_account )
    assert(agent_register)

    surferMock = SurferMock(config.surfer_url)

    model = SurferModel(ocean, agent_register[0], agent_register[1])
    SurferModel.set_http_client(surferMock)

    endpoint = model.get_endpoint('metadata', SurferAgent.endPointName)
    result = model.register_asset(metadata['base'], endpoint)
    assert(result)
    assert(result['asset_id'])
    assert(result['metadata_text'])
