"""


    Test Contract Manager


"""

from starfish.contract import ContractManager

def test_contract_load(network):
    manager = ContractManager(network.web3, 'starfish.contract')
    contract = manager.load('DirectPurchaseContract', network.name)
