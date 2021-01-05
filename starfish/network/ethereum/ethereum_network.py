"""

    Network class

    To access block chain network services.

"""

import logging
from typing import (
    Any,
    List
)
import requests

from web3 import (
    HTTPProvider,
    Web3
)

from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware import geth_poa_middleware

from starfish.exceptions import (
    StarfishConnectionError,
    StarfishInsufficientFunds
)
from starfish.network.did import is_did
from starfish.network.ethereum.ethereum_account import EthereumAccount
from starfish.network.network_base import NetworkBase
from starfish.types import (
    AccountAddress,
    ProvenanceEventList,
    TContractBase
)


logger = logging.getLogger(__name__)

DEFAULT_PACKAGE_NAME = 'starfish.network.ethereum.contract'

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
    'DatacraftToken': {
        'name': 'DatacraftTokenContract'
    },
    'Dispenser': {
        'name': 'DispenserContract'
    },
    'Provenance': {
        'name': 'ProvenanceContract',
    },

}


class EthereumNetwork(NetworkBase):
    def __init__(self, url: str, artifacts_path: str = None, load_development_contracts: bool = True) -> None:
        NetworkBase.__init__(self, url)
        self._web3 = None
        self._name = None
        self._id = None
        self._artifacts_path = artifacts_path
        self._contracts = {}
        if artifacts_path is None:
            artifacts_path = 'artifacts'

        from starfish.network.ethereum.contract.contract_manager import ContractManager

        if self._connect(self._url, artifacts_path):
            self._contract_manager = ContractManager(
                self,
                DEFAULT_PACKAGE_NAME,
                artifacts_path,
            )
            if load_development_contracts and self._name == 'local':
                self._contract_manager.load_local_artifacts_package()

    def get_contract(self, name: str) -> TContractBase:
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
    def get_ether_balance(self, account_address: AccountAddress) -> float:
        network_contract = self.get_contract('Network')
        return network_contract.get_balance(account_address)

    def get_token_balance(self, account_address: AccountAddress) -> float:
        datacraft_token_contract = self.get_contract('DatacraftToken')
        return datacraft_token_contract.get_balance(account_address)

    def request_test_tokens(self, account: EthereumAccount, amount: float) -> bool:
        dispenser_contract = self.get_contract('Dispenser')
        tx_hash = dispenser_contract.request_tokens(account, amount)
        receipt = dispenser_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def request_ether_from_faucet(self, account: EthereumAccount, url: str) -> None:
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
    def send_ether(self, account: EthereumAccount, to_account_address: AccountAddress, amount: float) -> bool:
        network_contract = self.get_contract('Network')

        account_balance = self.get_ether_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = network_contract.send_ether(account, to_account_address, amount)
        receipt = network_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def send_token(self, account: EthereumAccount, to_account_address: AccountAddress, amount: float) -> bool:
        datacraft_token_contract = self.get_contract('DatacraftToken')

        account_balance = self.get_token_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = datacraft_token_contract.transfer(account, to_account_address, amount)
        receipt = datacraft_token_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    """

    Send tokens (make payment) with logging

    """
    def send_token_and_log(
        self,
        account: EthereumAccount,
        to_account_address: AccountAddress,
        amount: float,
        reference_1: str = None,
        reference_2: str = None
    ) -> bool:
        datacraft_token_contract = self.get_contract('DatacraftToken')
        direct_contract = self.get_contract('DirectPurchase')

        account_balance = self.get_token_balance(account)
        if account_balance < amount:
            raise StarfishInsufficientFunds(f'The account has insufficient funds to send {amount} tokens')

        tx_hash = datacraft_token_contract.approve_transfer(
            account,
            direct_contract.address,
            amount
        )
        receipt = datacraft_token_contract.wait_for_receipt(tx_hash)
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

    def is_token_sent(
        self,
        from_account_address: AccountAddress,
        to_account_address: AccountAddress,
        amount: float,
        reference_1: str = None,
        reference_2: str = None
    ) -> bool:
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
    def register_provenace(self, account: EthereumAccount, asset_id: str) -> bool:
        provenance_contract = self.get_contract('Provenance')
        tx_hash = provenance_contract.register(account, asset_id)
        receipt = provenance_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def get_provenace_event_list(self, asset_id: str) -> ProvenanceEventList:
        provenance_contract = self.get_contract('Provenance')
        return provenance_contract.get_event_list(asset_id)

    """

    Register DID with a DDO and resolve DID to a DDO

    """
    def register_did(self, account: EthereumAccount, did: str, ddo_text: str) -> bool:
        did_registry_contract = self.get_contract('DIDRegistry')
        tx_hash = did_registry_contract.register(account, did, ddo_text)
        receipt = did_registry_contract.wait_for_receipt(tx_hash)
        return receipt.status == 1

    def resolve_did(self, did: str) -> str:
        ddo_text = None
        if did and is_did:
            did_registry_contract = self.get_contract('DIDRegistry')
            ddo_text = did_registry_contract.get_value(did)
        return ddo_text

    @property
    def contract_names(self) -> List[str]:
        return CONTRACT_LIST.keys()

    @property
    def name(self) -> str:
        return self._name

    @property
    def network_id(self) -> int:
        return self._id

    @property
    def web3(self) -> Any:
        return self._web3

    @staticmethod
    def find_network_name_from_id(network_id: int) -> str:
        if network_id in NETWORK_NAMES:
            return NETWORK_NAMES[network_id]
        return NETWORK_NAMES[0]

    def _connect(self, url: str, artifacts_path: str) -> bool:
        self._url = url
        self._web3 = Web3(HTTPProvider(url))
        if self._web3:

            try:
                self._id = int(self._web3.net.version)
                self._name = EthereumNetwork.find_network_name_from_id(self._id)
            except requests.exceptions.ConnectionError as e:
                raise StarfishConnectionError(e)

            if self._name == 'local':
                # inject the poa compatibility middleware to the innermost layer
                self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)

            logger.info(f'connected to the {self._name} network')
            self._web3.eth.setGasPriceStrategy(rpc_gas_price_strategy)
            return True
        return False

    def __str__(self) -> str:
        return f'Account: {self.address}'
