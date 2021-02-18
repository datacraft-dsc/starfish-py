"""
    starfish.did contract

"""
import re

from convex_api import ConvexAPI
from convex_api.utils import (
    is_address,
    to_address
)

from starfish.network.convex.contract.contract_base import ContractBase
from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.did import (
    did_to_id,
    id_to_did
)
from starfish.types import AccountAddress


class DIDContract(ContractBase):

    def __init__(self, convex: ConvexAPI):
        ContractBase.__init__(self, convex, 'starfish.did')

    def register_did(self, did: str, ddo_text: str, account: ConvexAccount):
        encode_ddo_text = re.sub('\\\\', '\\\\\\\\', ddo_text)
        encode_ddo_text = re.sub('"', '\\"', encode_ddo_text)
        did_id = did_to_id(did).lower()
        command = f'(register {did_id} "{encode_ddo_text}")'
        result = self.send(command, account)
        if result and 'value' in result:
            return id_to_did(result['value'])
        return result

    def resolve(self, did: str, account_address: AccountAddress):
        did_id = did_to_id(did).lower()
        command = f'(resolve {did_id})'
        if is_address(account_address):
            address = account_address
        else:
            address = account_address.address
        result = self.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result

    def owner(self, did: str,  account_address: AccountAddress):
        did_id = did_to_id(did).lower()
        command = f'(owner {did_id})'
        if is_address(account_address):
            address = account_address
        else:
            address = account_address.address
        result = self.query(command, address)
        if result and 'value' in result:
            return to_address(result['value'])
        return result
