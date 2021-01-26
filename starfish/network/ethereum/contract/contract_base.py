"""

    Contactt Base

"""
from typing import (
    Any,
    Generic
)

from starfish.network.ethereum.ethereum_account import EthereumAccount
from starfish.types import (
    AccountAddress,
    TContractBase
)

nonce_list = {}

GAS_MINIMUM = 200000


class ContractBase(Generic[TContractBase]):

    def __init__(self, name: str) -> None:
        self._name = name
        self._web3 = None
        self._abi = None
        self._address = None
        self._contract = None

    def load(self, web3: Any, abi: Any = None, address: str = None) -> None:
        self._web3 = web3
        self._abi = abi
        self._address = address
        self._contract = None
        if abi and address:
            self._contract = self._web3.eth.contract(
                address=address,
                abi=abi
            )

    def call(self, function_name: str, parameters: Any, account: EthereumAccount = None, transact: Any = None) -> Any:
        if self._contract is None:
            raise ValueError('contract not loaded')

        if not isinstance(parameters, (list, tuple)):
            parameters = (parameters,)

        contract_function_call = self._contract.functions[function_name](*parameters)
        if account:
            result = self._call_as_transaction(contract_function_call, account, transact)
            if result is None:
                raise ValueError(f'unable to sign a transaciton for {self.name}:{function_name}')
        else:
            result = contract_function_call.call()
        return result

    def get_event(self, event_name: str, parameters: Any = None) -> Any:
        if self._contract is None:
            raise ValueError('contract not loaded')
        return self._contract.events[event_name]

    def create_event_filter(
            self, event_name: str,
            parameters: Any = None,
            from_block: int = 1,
            argument_filters: Any = None
            ) -> Any:
        event = self.get_event(event_name, parameters)
        if event:
            return event.createFilter(
                fromBlock=from_block,
                argument_filters=argument_filters
            )
        return None

    def _call_as_transaction(self, contract_function_call: Any, account: EthereumAccount, transact: Any = None) -> str:
        if transact is None:
            gas_transact = {
                'from': account.address
            }
            gas = contract_function_call.estimateGas(gas_transact)
            transact = {
                'from': account.address,
                'gas': gas,
                'nonce': self.get_nonce(account.address)
            }

        built_transaction = contract_function_call.buildTransaction(transact)
        transaction = {
            'from': account.address,
            'to': built_transaction['to'],
            'gas': built_transaction['gas'],
            'data': built_transaction['data'],
            'gasPrice':  self.get_gas_price(account.address),
            'nonce':  built_transaction['nonce'],
        }
        signed = account.sign_transaction(transaction, self._web3)
        tx_hash = None
        if signed:
            tx_hash = self._web3.eth.sendRawTransaction(signed.rawTransaction)

        return tx_hash

    def wait_for_receipt(self, tx_hash: str, timeout: int = 30) -> Any:
        self._web3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)
        return self._web3.eth.getTransactionReceipt(tx_hash)

    def get_nonce(self, address: str) -> int:
        global nonce_list
        nonce = self._web3.eth.getTransactionCount(address)
        if address not in nonce_list:
            nonce_list[address] = nonce
        else:
            if nonce <= nonce_list[address]:
                nonce = nonce_list[address] + 1
        return nonce

    def get_gas_price(self, address: str) -> int:
        block = self._web3.eth.get_block("latest")
        gas_price = int(self._web3.eth.gasPrice / 100)
        gas_price = min(block.gasLimit, gas_price)
        gas_price = max(GAS_MINIMUM, gas_price)
        return gas_price

    def unlockAccount(self, account: EthereumAccount) -> None:
        self._web3.personal.unlockAccount(account.address, account.password)

    def lockAccount(self, account: EthereumAccount) -> None:
        self._web3.personal.lockAccount(account.address, account.password)

    @property
    def name(self) -> str:
        return self._name

    @property
    def web3(self) -> Any:
        return self._web3

    @property
    def address(self) -> str:
        return self._address

    def to_wei(self, amount_ether: float) -> int:
        return self._web3.toWei(amount_ether, 'ether')

    def to_ether(self, amount_wei: int) -> float:
        return self._web3.fromWei(amount_wei, 'ether')

    def get_account_address(self, account_address: AccountAddress) -> str:
        address = account_address
        if hasattr(account_address, 'address'):
            address = account_address.address

        if not self.web3.isChecksumAddress(address):
            address = self.web3.toChecksumAddress(address)

        return address
