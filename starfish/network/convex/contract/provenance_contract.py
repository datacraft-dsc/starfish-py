"""
    starfish.provenance contract

"""

from convex_api import ConvexAPI
from convex_api.utils import (
    is_address,
    to_address
)

from eth_utils import add_0x_prefix

from starfish.network.convex.contract.contract_base import ContractBase
from starfish.network.convex.convex_account import ConvexAccount
from starfish.types import AccountAddress


class ProvenanceContract(ContractBase):

    def __init__(self, convex: ConvexAPI):
        ContractBase.__init__(self, convex, 'starfish.provenance')

    def register(self, asset_id: str, account: ConvexAccount):
        command = f'(register {add_0x_prefix(asset_id)})'
        result = self.send(command, account)
        if result and 'value' in result:
            return {
                'timestamp': result['value']['timestamp'],
                'asset_id': add_0x_prefix(result['value']['asset-id']),
                'owner': to_address(result['value']['owner']),
            }
        return result

    def event_list(self, asset_id: str, account_address: AccountAddress):
        command = f'(event-list {add_0x_prefix(asset_id)})'
        if is_address(account_address):
            address = account_address
        else:
            address = account_address.address
        result = self.query(command, address)
        if result and 'value' in result:
            return ProvenanceContract.convert_event_list(result['value'])
        return result

    def event_owner(self, account_address: AccountAddress):
        if is_address(account_address):
            address = account_address
        else:
            address = account_address.address
        command = f'(event-owner {address})'
        result = self.query(command, address)
        if result and 'value' in result:
            return ProvenanceContract.convert_event_list(result['value'])
        return result

    @staticmethod
    def convert_event_list(items):
        event_list = []
        for item in items:
            event_list.append({
                'timestamp': item['timestamp'],
                'asset_id': add_0x_prefix(item['asset-id']),
                'owner': to_address(item['owner']),
            })
        return event_list
