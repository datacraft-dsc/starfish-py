"""


    Test Contract Manager


"""
from starfish.network.ethereum.ethereum_network import EthereumNetwork
from starfish.network.ethereum.contract.contract_manager import ContractManager

def test_contract_load_local_artiacts_package(config):
    # test pre-loaded contracts from non local test nodes
    network = EthereumNetwork(config['ethereum']['network']['url'], None, False)
    manager = ContractManager(network, 'starfish.network.ethereum.contract', 'artifacts')
    manager.load_local_artifacts_package()
    contract = manager.load('DIDRegistryContract')
