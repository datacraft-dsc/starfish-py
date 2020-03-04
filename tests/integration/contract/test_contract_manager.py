"""


    Test Contract Manager


"""

from starfish.contract import ContractManager

def test_contract_load(config):
    manager = ContractManager(config.keeper_url)
    contract = manager.load('direct_purchase_contract')