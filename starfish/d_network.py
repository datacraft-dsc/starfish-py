"""

    DNetwork class


"""

import logging
import re
import time
import requests

from web3 import (
    HTTPProvider,
    Web3
)
from web3.gas_strategies.rpc import rpc_gas_price_strategy

from starfish.contract import ContractManager
from starfish.exceptions import (
    StarfishConnectionError,
    StarfishInsufficientFunds
)
from starfish.utils.local_node import get_local_contract_files


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
        'has_artifact': False,
    },
    'DIDRegistry': {
        'name': 'DIDRegistryContract',
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
    },

}


class DNetwork():
    def __init__(self, url):
        self._url = url
        self._web3 = None
        self._name = None
        self._contracts = {}
        self._connect(self._url)

    def load_development_contracts(self, timeout_seconds=240, sleep_time_seconds=10):
        """

        This only need to be called on a development network, where the contracts are installed locally on the local node/network.

        Wait for the contracts to be ready and installed

        """

        # only do this for the local 'spree' or 'development' node

        if not self._name == 'spree' or self._name == 'development':
            return True

        # This list order is important, the development contracts have priority over spree
        test_network_name_list = ['development', 'spree']
        if timeout_seconds is None:
            timeout_seconds = 240
        timeout_time = time.time() + timeout_seconds
        while timeout_time > time.time():
            load_items = get_local_contract_files('keeper-contracts', '/keeper-contracts/artifacts')

            # now go through the list and collate the contract artifacts to a dict
            # we give pereference for .development. contracts
            contract_items = {}

            for filename, data in load_items.items():
                if 'name' in data:
                    match = re.match(r'(\w+)\.(\w+)\.json', filename)
                    if match:
                        contract_name = match.group(1)
                        network_name = match.group(2)
                        if network_name and network_name in test_network_name_list:
                            if network_name not in contract_items:
                                contract_items[network_name] = {}
                            contract_items[network_name][contract_name] = data

            # now go through the list of contracts supported and load in the artifact data
            load_count = 0
            contract_count = 0
            for contract_name, item in CONTRACT_LIST.items():
                if item.get('has_artifact', True):
                    contract_count += 1
                    for network_name in test_network_name_list:
                        if network_name in contract_items and contract_name in contract_items[network_name]:
                            data = contract_items[network_name][contract_name]
                            self._contract_manager.set_contract_data(contract_name, data)
                            logger.debug(f'imported contract {contract_name}.{network_name}')
                            load_count += 1
                            break
            if load_count == contract_count:
                return True
            # take some sleep to wait for the contracts to be built
            logger.debug(f'only loaded {load_count} out of {contract_count} contracts wating for local node to startup..')
            time.sleep(sleep_time_seconds)
        return False

    def get_contract(self, name):
        if name not in CONTRACT_LIST:
            raise LookupError(f'Invalid contract name: {name}')

        if name not in self._contracts:
            item = CONTRACT_LIST[name]
            self._contracts[name] = self._contract_manager.load(
                item['name'],
                artifact_filename=item.get('artifact_filename', None),
                has_artifact=item.get('has_artifact', True)
            )
        return self._contracts[name]

    """

    Account based operations


    """
    def get_ether_balance(self, account):
        network_contract = self.get_contract('Network')
        return network_contract.get_balance(account.address)

    def get_token_balance(self, account):
        ocean_token_contract = self.get_contract('OceanToken')
        return ocean_token_contract.get_balance(account)

    def request_test_tokens(self, account, amount):
        dispenser_contract = self.get_contract('Dispenser')
        tx_hash = dispenser_contract.request_tokens(account, amount)
        receipt = dispenser_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def request_ether_from_faucet(self, account, url):
        data = {
            'address': account.address,
            'agent': 'server',
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=data, headers=headers)
        logger.debug(f'response {response.text} {response.status_code}')
        if response.status_code != 200:
            logger.warning(f'{response.status_code} {response.text}')

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
            try:
                self._name = DNetwork.find_network_name_from_id(int(self._web3.net.version))
            except requests.exceptions.ConnectionError as e:
                raise StarfishConnectionError(e)

            logger.info(f'connected to the {self._name} network')
            self._web3.eth.setGasPriceStrategy(rpc_gas_price_strategy)
            self._contract_manager = ContractManager(self._web3, self._name, DEFAULT_PACKAGE_NAME)
            return True
        return False
