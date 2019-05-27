from unittest.mock import Mock
import pytest
import secrets
import logging

from tests.integration.libs.integration_test_config import integrationTestConfig

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.models.surfer_model import SurferModel

from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.brizo.brizo import Brizo
from tests.integration.mocks.brizo_mock import BrizoMock



@pytest.fixture(scope="module")
def ocean():
    ocean = Ocean(keeper_url=integrationTestConfig.keeper_url,
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
    return integrationTestConfig


@pytest.fixture(scope="module")
def surfer_agent(ocean):

    integrationTestConfig.authorization=SurferModel.get_authorization_token(
        integrationTestConfig.surfer_url,
        integrationTestConfig.surfer_username,
        integrationTestConfig.surfer_password
    )

    ddo = SurferAgent.generate_ddo(integrationTestConfig.surfer_url)
    options = {
        'url': integrationTestConfig.surfer_url,
        'username': integrationTestConfig.surfer_username,
        'password': integrationTestConfig.surfer_password
    }
    return SurferAgent(ocean, did=ddo.did, ddo=ddo, options=options)
