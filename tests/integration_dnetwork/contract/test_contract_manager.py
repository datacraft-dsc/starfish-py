"""


    Test Contract Manager


"""

from starfish.contract import ContractManager

def test_contract_load(dnetwork):
    manager = ContractManager(dnetwork.web3, 'starfish.contract')
    contract = manager.load('DirectPurchaseContract', dnetwork.network_name)
