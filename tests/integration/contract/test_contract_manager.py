"""


    Test Contract Manager


"""

from starfish.contract import ContractManager

def test_contract_load(network):
    # test pre-loaded contracts from non local test nodes

    manager = ContractManager(network.web3, 'nile', 'starfish.contract')
    contract = manager.load('DIDRegistryContract')
