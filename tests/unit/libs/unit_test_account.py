import secrets

from eth_account import Account as EthAccount
from web3 import Web3

class UnitTestAccount():

    def __init__(self, password=None):
        self.password = secrets.token_hex(32)
        if password:
            self.password = password
        local_account = EthAccount.create(password)
        self.key_data = EthAccount.encrypt(local_account.key, password)
        self.address = Web3.toChecksumAddress(self.key_data['address'])

