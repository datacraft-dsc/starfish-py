"""

    Contactt Base

"""

nonce_list = {}


class ContractBase:

    def __init__(self, name):
        self._name = name
        self._web3 = None
        self._abi = None
        self._address = None
        self._contract = None
        self._gas_price = 0

    def load(self, web3, abi=None, address=None):
        self._web3 = web3
        self._abi = abi
        self._address = address
        self._contract = self._web3.eth.contract(
            address=address,
            abi=abi
        )

    def call(self, function_name, parameters, account=None):
        if not isinstance(parameters, (list, tuple)):
            parameters = (parameters,)

        if account:
            result = self._call_with_transaction(function_name, parameters, account)
        else:
            result = self._contract.functions[function_name](*parameters).call()
        return result

    def _call_with_transaction(self, function_name, parameters, account):
        # return self._contract.caller(transaction=transaction).function_name(*parameters)
        transact = {
            'gas': self.get_gas_price(account.address),
            'nonce': self.get_nonce(account.address),
        }
        transaction = self._contract.functions[function_name](*parameters).buildTransaction(transact)
        signed = account.sign_transaction(self._web3, transaction)
        tx_hash = None
        if signed:
            tx_hash = self._web3.eth.sendRawTransaction(signed.rawTransaction)
        return tx_hash

    def wait_for_receipt(self, tx_hash):
        return self._web3.eth.waitForTransactionReceipt(tx_hash, timeout=30)

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
        self._gas_price = int(self._web3.eth.gasPrice / 100)
        self._gas_price = max(self._gas_price, block.gasLimit)
        return self._gas_price

    @property
    def name(self):
        return self._name

    @property
    def web3(self):
        return self._web3

    @property
    def address(self):
        return self._address
