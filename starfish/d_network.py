"""

    DNetwork class


"""

import logging

from web3 import HTTPProvider, Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

from starfish.contract import ContractManager

logger = logging.getLogger(__name__)

DEFAULT_PACKAGE_NAME = 'starfish.contract'

NETWORK_NAMES = {
    0: 'development',
    1: 'main',
    2: 'morden',
    3: 'ropsten',
    4: 'rinkeby',
    42: 'kovan',
    8995: 'nile',           # Ocean Protocol Public test net
    8996: 'spree'           # Ocean Protocol local test net
}

CONTRACT_LIST = {
    'DIDRegistry': {
        'name': 'DIDRegistryContract',
        'abi_filename': 'DIDRegistry.development.json'
    },
    'DirectPurchase': {
        'name': 'DirectPurchaseContract'
    },
    'OceanToken': {
        'name': 'OceanTokenContract'
    },
    'Dispenser': {
        'name': 'DispenserContract'
    },
    'Provenance': {
        'name': 'ProvenanceContract',
        'abi_filename': 'Provenance.development.json'
    },

}


class DNetwork():
    def __init__(self, network_url):
        self._network_url = network_url
        self._web3 = None
        self._network_name = None
        self._contracts = {}
        self._web3 = Web3(HTTPProvider(self._network_url))
        if self._web3:
            self._network_name = DNetwork.find_network_name_from_id(int(self._web3.version.network))
            logger.info(f'connected to {self._network_name}')
            self._web3.eth.setGasPriceStrategy(rpc_gas_price_strategy)
            self._contract_manager = ContractManager(self._web3, DEFAULT_PACKAGE_NAME)

    def get_contract(self, name):
        if name not in CONTRACT_LIST:
            raise LookupError(f'Invalid contract name: {name}')

        if name not in self._contracts:
            item = CONTRACT_LIST[name]
            self._contracts[name] = self._contract_manager.load(item['name'], self._network_name, item.get('abi_filename', None))
        return self._contracts[name]

    def get_ether_balance(self, account):
        return self._web3.eth.getBalance(account.address)

    def get_token_balance(self, account):
        ocean_token_contract = self.get_contract('OceanToken')
        return ocean_token_contract.get_balance(account)

    def request_test_tokens(self, amount, account):
        dispenser_contract = self.get_contract('Dispenser')
        tx_hash = dispenser_contract.request_tokens(amount, account)
        receipt = dispenser_contract.wait_for_receipt(tx_hash)


    @property
    def contract_names(self):
        return CONTRACT_LIST.keys()

    @property
    def network_url(self):
        return self._network_url

    @property
    def network_name(self):
        return self._network_name

    @property
    def web3(self):
        return self._web3

    @staticmethod
    def find_network_name_from_id(network_id):
        if network_id in NETWORK_NAMES:
            return NETWORK_NAMES[network_id]
        return NETWORK_NAMES[0]
