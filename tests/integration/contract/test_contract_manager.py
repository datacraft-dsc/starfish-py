"""


    Test Contract Manager


"""
from starfish import Network
from starfish.contract import ContractManager

def test_contract_load_local_artiacts_package(config):
    # test pre-loaded contracts from non local test nodes
    network = Network(config['network']['url'], None, False)
    manager = ContractManager(network.web3, 1337, 'local', 'starfish.contract', 'artifacts')
    manager.load_local_artifacts_package()
    contract = manager.load('DIDRegistryContract')
