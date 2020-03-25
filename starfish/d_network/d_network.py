"""

    DNetwork class


"""

import logging

from web3 import (
    HTTPProvider,
    Web3
)
from web3.gas_strategies.rpc import rpc_gas_price_strategy

from starfish.contract import ContractManager
from starfish.exceptions import StarfishInsufficientFunds

logger = logging.getLogger(__name__)

DEFAULT_PACKAGE_NAME = 'starfish.contract'

NETWORK_NAMES = {
    0: 'development',
    1: 'main',
    2: 'morden',
    3: 'ropsten',
    4: 'rinkeby',
    42: 'kovan',
    77: 'POA_Sokol',
    99: 'POA_Core',
    100: 'xDai',
    8995: 'nile',                   # Ocean Protocol Public test net
    8996: 'spree',                  # Ocean Protocol local test net
    0xcea11: 'pacific'              # Ocean Protocol Public mainnet
}

CONTRACT_LIST = {
    'Network': {
        'name': 'NetworkContract',
        'abi_filename': False,
    },
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
    def __init__(self, url):
        self._url = url
        self._web3 = None
        self._name = None
        self._contracts = {}
        self._connect(self._url)

    def get_contract(self, name):
        if name not in CONTRACT_LIST:
            raise LookupError(f'Invalid contract name: {name}')

        if name not in self._contracts:
            item = CONTRACT_LIST[name]
            self._contracts[name] = self._contract_manager.load(item['name'], self._name, item.get('abi_filename', None))
        return self._contracts[name]

    """

    Account based operations

    """
    def get_ether_balance(self, account_address):
        network_contract = self.get_contract('Network')
        return network_contract.get_balance(account_address)

    def get_token_balance(self, account):
        ocean_token_contract = self.get_contract('OceanToken')
        return ocean_token_contract.get_balance(account)

    def request_test_tokens(self, account, amount):
        dispenser_contract = self.get_contract('Dispenser')
        tx_hash = dispenser_contract.request_tokens(account, amount)
        receipt = dispenser_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    """

    Send ether and tokens to another account

    """
    def send_ether(self, account, to_account_address, amount):
        network_contract = self.get_contract('Network')

        account_balance = self.get_ether_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = network_contract.send_ether(account, to_account_address, amount)
        receipt = network_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def send_token(self, account, to_account_address, amount):
        ocean_token_contract = self.get_contract('OceanToken')

        account_balance = self.get_token_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = ocean_token_contract.transfer(account, to_account_address, amount)
        receipt = ocean_token_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    """

    Send tokens (make payment) with logging

    """
    def send_token_and_log(self, account, to_account_address, amount, reference_1=None, reference_2=None):
        ocean_token_contract = self.get_contract('OceanToken')
        direct_contract = self.get_contract('DirectPurchase')

        account_balance = self.get_token_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = ocean_token_contract.approve_transfer(
            account,
            direct_contract.address,
            amount
        )
        receipt = ocean_token_contract.wait_for_receipt(tx_hash)
        if receipt and receipt.status == 1:
            tx_hash = direct_contract.send_token_and_log(
                account,
                to_account_address,
                amount,
                reference_1,
                reference_2
            )
            receipt = direct_contract.wait_for_receipt(tx_hash)
            if receipt and receipt.status == 1:
                return True
        return False

    def is_token_sent(self, from_account_address, to_account_address, amount, reference_1=None, reference_2=None):
        direct_contract = self.get_contract('DirectPurchase')

        is_sent = direct_contract.check_is_paid(
            from_account_address,
            to_account_address,
            amount,
            reference_1,
            reference_2
        )
        return is_sent

    """

    Register Provenance

    """
    def register_provenace(self, account, asset_id):
        provenance_contract = self.get_contract('Provenance')
        tx_hash = provenance_contract.register(account, asset_id)
        receipt = provenance_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def get_provenace_event_list(self, asset_id):
        provenance_contract = self.get_contract('Provenance')
        return provenance_contract.get_event_list(asset_id)

    """

    Register DID with a DDO and resolve DID to a DDO

    """
    def register_did(self, account, did, ddo_text):
        did_registry_contract = self.get_contract('DIDRegistry')
        tx_hash = did_registry_contract.register(account, did, ddo_text)
        receipt = did_registry_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def resolve_did(self, did):
        did_registry_contract = self.get_contract('DIDRegistry')
        return did_registry_contract.get_value(did)

    @property
    def contract_names(self):
        return CONTRACT_LIST.keys()

    @property
    def url(self):
        return self._url

    @property
    def name(self):
        return self._name

    @property
    def web3(self):
        return self._web3

    @staticmethod
    def find_network_name_from_id(network_id):
        if network_id in NETWORK_NAMES:
            return NETWORK_NAMES[network_id]
        return NETWORK_NAMES[0]

    def _connect(self, url):
        self._url = url
        self._web3 = Web3(HTTPProvider(url))
        if self._web3:
            self._name = DNetwork.find_network_name_from_id(int(self._web3.net.version))
            logger.info(f'connected to the {self._name} network')
            self._web3.eth.setGasPriceStrategy(rpc_gas_price_strategy)
            self._contract_manager = ContractManager(self._web3, DEFAULT_PACKAGE_NAME)
            return True
        return False
