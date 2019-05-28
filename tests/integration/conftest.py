from unittest.mock import Mock
import pytest
import secrets
import logging
import pathlib

from tests.integration.libs.integration_test_config import IntegrationTestConfig

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.models.surfer_model import SurferModel

CONFIG_FILE_PATH = pathlib.Path.cwd() / 'tests' / 'integration' / 'config.ini'
INVOKE_CONFIG_FILE_PATH = pathlib.Path.cwd() / 'tests' / 'integration' / 'invoke_config.ini'


@pytest.fixture(scope="module")
def ocean():
    integrationTestConfig = IntegrationTestConfig(CONFIG_FILE_PATH)    
    ocean = Ocean(
        keeper_url=integrationTestConfig.keeper_url,
        contracts_path=integrationTestConfig.contracts_path,
        gas_limit=integrationTestConfig.gas_limit,
        log_level=logging.WARNING
    )

    return ocean

@pytest.fixture(scope="module")
def brizo_mock():
    BrizoProvider.set_brizo_class(BrizoMock)
    mock = BrizoProvider.get_brizo()
    return mock

@pytest.fixture(scope="module")
def config():
    integrationTestConfig = IntegrationTestConfig(CONFIG_FILE_PATH)
    return integrationTestConfig


@pytest.fixture(scope="module")
def surfer_agent(ocean):
    print(ocean)
    integrationTestConfig = IntegrationTestConfig(CONFIG_FILE_PATH)

    ddo = SurferAgent.generate_ddo(integrationTestConfig.surfer_url)
    options = {
        'url': integrationTestConfig.surfer_url,
        'username': integrationTestConfig.surfer_username,
        'password': integrationTestConfig.surfer_password,
        'authorization': SurferModel.get_authorization_token(
            integrationTestConfig.surfer_url,
            integrationTestConfig.surfer_username,
            integrationTestConfig.surfer_password
        )
    }
    return SurferAgent(ocean, did=ddo.did, ddo=ddo, options=options)

@pytest.fixture(scope="module")
def invoke_config():
    integrationTestConfig = IntegrationTestConfig(INVOKE_CONFIG_FILE_PATH)
    return integrationTestConfig

@pytest.fixture(scope="module")
def invoke_surfer_agent(ocean):
    integrationTestConfig = IntegrationTestConfig(INVOKE_CONFIG_FILE_PATH)
    ddo = SurferAgent.generate_ddo(integrationTestConfig.surfer_url)
    options = {
        'url': integrationTestConfig.surfer_url,
        'username': integrationTestConfig.surfer_username,
        'password': integrationTestConfig.surfer_password
    }
    return SurferAgent(ocean, did=ddo.did, ddo=ddo, options=options)


