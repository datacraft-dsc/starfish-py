"""
    Test Surfer ddo resolver class

"""

import pathlib
import json
import logging
import time
from web3 import Web3
import requests
import pytest

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.asset import MemoryAsset
from tests.integration.mocks.surfer_mock import SurferMock
from starfish.models.surfer_model import SurferModel


def test_get_ddo(ocean, metadata, config):

    ## Needs the test resolveer to be available in Barge+Surfer
    surfer_url='http://localhost:8080/'

    username='Aladdin'
    password='OpenSesame'
    auth=(username,password)
    did="did:ocn:950d6a6111abf7acef5d85b3e6733846a8a01baa7b602a2e091accab69d980df"
    data={"did":did, 
            "ddo":{ "service": [{ "serviceEndpoint": "http://localhost:8080/api/v1/meta", "type": "Ocean.Meta.v1" }, 
                { "serviceEndpoint": "http://localhost:8080/api/v1/assets", "type": "Ocean.Storage.v1" }, 
                { "serviceEndpoint": "http://localhost:8080/api/v1/invoke", "type": "Ocean.Invoke.v1" }, 
                { "serviceEndpoint": "http://localhost:8080/api/v1/market", "type": "Ocean.Market.v1" }]}}
    ## First create the DDO entry
    response=requests.post(surfer_url+'api/v1/test-resolver/',json=data,auth=auth)
    assert response is not None
    
    ##retrieve the DDO
    ddo = SurferAgent.get_ddo(did,surfer_url,auth)
    assert ddo['service'] is not None 

    ## verify that unknown DIDs raise ValueError
    with pytest.raises(ValueError):
        ddo = SurferAgent.get_ddo('abcd',surfer_url,auth)
