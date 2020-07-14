"""

    DIDRegistry Contract

"""

import datetime
import logging
from eth_utils import remove_0x_prefix

from starfish.account import Account
from starfish.contract.contract_base import ContractBase
from starfish.types import ProvenanceEventList

logger = logging.getLogger(__name__)

CONTRACT_NAME = 'Provenance'


class ProvenanceContract(ContractBase):
    """

    Class representing the DIDRegistry contract.

    """

    def __init__(self) -> None:
        ContractBase.__init__(self, CONTRACT_NAME)

    def register(self, account: Account, asset_id: str) -> str:
        asset_id_bytes = self._web3.toBytes(hexstr=asset_id)
        tx_hash = self.call('registerAsset', (asset_id_bytes), account)
        return tx_hash

    def get_block_number(self, asset_id: str) -> int:
        asset_id_bytes = self._web3.toBytes(hexstr=asset_id)
        block_number = self.call('getBlockNumber', asset_id_bytes)
        return block_number

    def get_event_list(self, asset_id: str) -> ProvenanceEventList:
        result = []
        from_block_number = self.get_block_number(asset_id)
        if from_block_number:
            asset_id_bytes = self._web3.toBytes(hexstr=asset_id)
            event_filter = self.create_event_filter(
                'AssetRegistered',
                None,
                from_block=from_block_number,
                argument_filters={'_assetID': asset_id_bytes}
            )

            if event_filter:
                for event_log in event_filter.get_all_entries():
                    event_args = event_log.args
                    event_asset_id = remove_0x_prefix(self._web3.toHex(event_args['_assetID']))
                    if remove_0x_prefix(event_asset_id) == remove_0x_prefix(asset_id):
                        item = {
                            'asset_id': event_asset_id,
                            'account': event_args['_user'],
                            'timestamp': datetime.datetime.fromtimestamp(event_args['_timestamp'])
                        }
                        result.append(item)
        return result
