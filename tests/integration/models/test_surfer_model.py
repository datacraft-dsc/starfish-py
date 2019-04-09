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
import tests.integration.utils.ddo as ddo

from tests.integration.mocks.surfer_mock import SurferMock


def test_register_asset(ocean, metadata, config):
    did,ddoval=ddo.get_ddo(config)
    assert did is not None
    assert ddoval is not None

    surfer=SurferAgent(ocean,did=did,ddo=ddoval,options={'authorization':config.authorization})
    assert surfer is not None

    surferMock = SurferMock(config.surfer_url)

    model = surfer._get_surferModel(did=did,ddo=ddoval)
    SurferModel.set_http_client(surferMock)

    #result = model.register_asset(metadata['base'])
    #assert(result)
    #assert(result['asset_id'])
    #assert(result['metadata_text'])
