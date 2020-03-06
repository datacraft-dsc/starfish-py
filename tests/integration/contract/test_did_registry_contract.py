import pytest


from starfish.contract import ContractManager
from starfish.utils import did_generate_random
from starfish.agent import RemoteAgent


def test_did_registry_contract(config, starfish_accounts):
    """

    Register and find a ddo based on a did

    """
    manager = ContractManager(config.keeper_url)
    did_registry_contract = manager.load('DIDRegistryContract')

    did = did_generate_random()

    services = Services(config.remote_agent_url, all_services=True)
    ddo = RemoteAgent.generate_ddo(services)

    register_account = starfish_accounts['purchaser']


    did_registry_contract.register(register_account, did, ddo)
