from unittest.mock import Mock
import pytest
import secrets

from tests.unit.libs.unit_test_config import unitTestConfig
from starfish import Ocean
from tests.unit.mocks.mock_squid_agent_adapter import MockSquidAgentAdapter



@pytest.fixture(scope="module")
def ocean():
    result = Ocean(keeper_url=unitTestConfig.keeper_url,
            contracts_path=unitTestConfig.contracts_path,
            gas_limit=unitTestConfig.gas_limit,
            squid_agent_adapter_class=MockSquidAgentAdapter,
            connect=False
    )
    return result

@pytest.fixture(scope="module")
def config():
    return unitTestConfig
