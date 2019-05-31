from unittest.mock import Mock
import pytest
import secrets
import logging
import pathlib

from tests.integration.libs.integration_test_config import IntegrationTestConfig

from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.brizo.brizo import Brizo

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.models.surfer_model import SurferModel

from tests.integration.mocks.brizo_mock import BrizoMock

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
    integrationTestConfig = IntegrationTestConfig(CONFIG_FILE_PATH)

    ddo_options = None
    if integrationTestConfig.koi_url:
        ddo_options = {
            'invoke': f'{integrationTestConfig.koi_url}/api/v1',
        }
    ddo = SurferAgent.generate_ddo(integrationTestConfig.surfer_url, ddo_options)
    options = {
        'url': integrationTestConfig.surfer_url,
        'username': integrationTestConfig.surfer_username,
        'password': integrationTestConfig.surfer_password,
    }
    return SurferAgent(ocean, did=ddo.did, ddo=ddo, options=options)
