from unittest.mock import Mock
import pytest
import secrets
import logging

from tests.integration.libs.integration_test_config import integrationTestConfig

from starfish import Ocean



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
