from unittest.mock import Mock
import pytest
import secrets

from tests.unit.test_config import testConfig

from starfish import Ocean

from tests.mocks.mock_squid_model import MockSquidModel



@pytest.fixture(scope="module")
def ocean():
    result = Ocean(keeper_url=testConfig.keeper_url,
            contracts_path=testConfig.contracts_path,
            gas_limit=testConfig.gas_limit,
            squid_model_class=MockSquidModel
    )
    return result
