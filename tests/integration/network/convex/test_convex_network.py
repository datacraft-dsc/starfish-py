"""

    Test Convex Network class

"""
import pytest
import secrets

from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services


TEST_AMOUNT = 5


def test_convex_network_setup(convex_network, config):
    assert(convex_network.url == config['convex']['network']['url'])
