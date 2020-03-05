"""

    Contactt Base

"""

nonce_list = {}

GAS_MINIMUM = 200000

class ContractBase:

    def __init__(self, name):
        self._name = name
        self._web3 = None
        self._abi = None
        self._address = None
        self._contract = None

    def load(self, web3, abi=None, address=None):
        self._web3 = web3
        self._abi = abi
        self._address = address
        self._contract = self._web3.eth.contract(
            address=address,
            abi=abi
        )

    def call(self, function_name, parameters, account=None, transact=None):
        if not isinstance(parameters, (list, tuple)):
            parameters = (parameters,)

        if account:
            result = self._call_as_transaction(function_name, parameters, account, transact)
        else:
            result = self._contract.functions[function_name](*parameters).call()
        return result

    def _call_as_transaction(self, function_name, parameters, account, transact=None):
        if transact is None:
            transact = {
                'gas': self.get_gas_price(account.address),
                'nonce': self.get_nonce(account.address),
            }
        built_transaction = self._contract.functions[function_name](*parameters).buildTransaction(transact)
        transaction = {
            'from': account.address,
            'to': built_transaction['to'],
            'gasPrice':  self.get_gas_price(account.address),
            'nonce':  built_transaction['nonce'],
            'gas': built_transaction['gas'],
            'data': built_transaction['data'],
        }
        print(transaction)
        signed = account.sign_transaction(self._web3, transaction)
        tx_hash = None
        if signed:
            tx_hash = self._web3.eth.sendRawTransaction(signed.rawTransaction)
        else:
            raise ValueError(f'unable to sign a transaciton for {self.name}:{function_name}')

        return tx_hash

    def wait_for_receipt(self, tx_hash, timeout=30):
        return self._web3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)

    def get_nonce(self, address):
        global nonce_list
        nonce = self._web3.eth.getTransactionCount(address)
        if address not in nonce_list:
            nonce_list[address] = nonce
        else:
            if nonce <= nonce_list[address]:
                nonce = nonce_list[address] + 1
        return nonce

    def get_gas_price(self, address):
        block = self._web3.eth.getBlock("latest")
        gas_price = int(self._web3.eth.gasPrice / 100)
        gas_price = min(block.gasLimit, gas_price)
        gas_price = max(GAS_MINIMUM, gas_price)
        return gas_price

    @property
    def name(self):
        return self._name

    @property
    def web3(self):
        return self._web3

    @property
    def address(self):
        return self._address
