"""

    Network class

    To access block chain network services.

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
from web3.middleware import geth_poa_middleware

from starfish.contract import ContractManager
from starfish.ddo import create_ddo_object
from starfish.exceptions import (
    StarfishConnectionError,
    StarfishInsufficientFunds
)
from starfish.utils.did import is_did
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
    1337: 'local',                  # Local private network
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
    'DexToken': {
        'name': 'DexTokenContract'
    },
    'Dispenser': {
        'name': 'DispenserContract'
    },
    'Provenance': {
        'name': 'ProvenanceContract',
    },

}


class Network():
    def __init__(self, url, artifacts_path=None, load_development_contracts=True):
        self._url = url
        self._web3 = None
        self._name = None
        self._id = None
        self._artifacts_path = artifacts_path
        self._contracts = {}
        if artifacts_path is None:
            artifacts_path = 'artifacts'
        if self._connect(self._url, artifacts_path):
            self._contract_manager = ContractManager(
                self._web3,
                self._id,
                self._name,
                DEFAULT_PACKAGE_NAME,
                artifacts_path,
            )
            if load_development_contracts and self._name == 'local':
                self._contract_manager.load_local_artifacts_package()

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
    def get_ether_balance(self, account_address):
        network_contract = self.get_contract('Network')
        return network_contract.get_balance(account_address)

    def get_token_balance(self, account_address):
        dex_token_contract = self.get_contract('DexToken')
        return dex_token_contract.get_balance(account_address)

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
        dex_token_contract = self.get_contract('DexToken')

        account_balance = self.get_token_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = dex_token_contract.transfer(account, to_account_address, amount)
        receipt = dex_token_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    """

    Send tokens (make payment) with logging

    """
    def send_token_and_log(self, account, to_account_address, amount, reference_1=None, reference_2=None):
        dex_token_contract = self.get_contract('DexToken')
        direct_contract = self.get_contract('DirectPurchase')

        account_balance = self.get_token_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = dex_token_contract.approve_transfer(
            account,
            direct_contract.address,
            amount
        )
        receipt = dex_token_contract.wait_for_receipt(tx_hash)
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
        ddo_text = None
        if did and is_did:
            did_registry_contract = self.get_contract('DIDRegistry')
            ddo_text = did_registry_contract.get_value(did)
        return ddo_text

    """


    Helper methods


    """

    def resolve_agent(self, agent_url_did, username=None, password=None, authentication=None):

        # stop circular references on import

        from starfish.agent.remote_agent import RemoteAgent

        ddo = None
        if is_did(agent_url_did):
            ddo_text = self.resolve_did(agent_url_did)
            if ddo_text:
                ddo = create_ddo_object(ddo_text)
            return ddo

        if not authentication:
            if username or password:
                authentication = {
                    'username': username,
                    'password': password
                }
        ddo_text = RemoteAgent.resolve_url(agent_url_did, authentication)
        if ddo_text:
            ddo = create_ddo_object(ddo_text)
        return ddo

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

    def _connect(self, url, artifacts_path):
        self._url = url
        self._web3 = Web3(HTTPProvider(url))
        if self._web3:

            try:
                self._id = int(self._web3.net.version)
                self._name = Network.find_network_name_from_id(self._id)
            except requests.exceptions.ConnectionError as e:
                raise StarfishConnectionError(e)

            if self._name == 'local':
                # inject the poa compatibility middleware to the innermost layer
                self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)

            logger.info(f'connected to the {self._name} network')
            self._web3.eth.setGasPriceStrategy(rpc_gas_price_strategy)
            return True
        return False