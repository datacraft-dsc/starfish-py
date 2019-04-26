from unittest.mock import Mock
import pytest
import secrets
import logging

from tests.integration.libs.integration_test_config import integrationTestConfig

from starfish import Ocean
from starfish.agent import SurferAgent




@pytest.fixture(scope="module")
def ocean():
    result = Ocean(keeper_url=integrationTestConfig.keeper_url,
            contracts_path=integrationTestConfig.contracts_path,
            gas_limit=integrationTestConfig.gas_limit,
            log_level=logging.WARNING
    )
    return result

@pytest.fixture(scope="module")
def config():
    return integrationTestConfig


@pytest.fixture(scope="module")
def surfer_agent(ocean):


    ddo = SurferAgent.generate_ddo(integrationTestConfig.surfer_url)
    options = {
        'url': integrationTestConfig.surfer_url,
        'username': integrationTestConfig.surfer_username,
        'password': integrationTestConfig.surfer_password
    }
    return SurferAgent(ocean, did=ddo.did, ddo=ddo, options=options)
