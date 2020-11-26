"""

    DIDRegistry Contract

"""

import logging

from starfish.network.did import did_to_id
from starfish.network.ethereum.contract.contract_base import ContractBase
from starfish.network.ethereum.ethereum_account import EthereumAccount

logger = logging.getLogger(__name__)

CONTRACT_NAME = 'DIDRegistry'

MAX_DDO_TEXT_SIZE = 2048


class DIDRegistryContract(ContractBase):
    """

    Class representing the DIDRegistry contract.

    """

    def __init__(self) -> None:
        ContractBase.__init__(self, CONTRACT_NAME)

    def register(self, account: EthereumAccount, did: str, ddo_text: str) -> str:
        tx_hash = None
        did_id = did_to_id(did)
        if did_id:
            did_id = self._web3.toBytes(hexstr=did_id)
            if len(ddo_text) > MAX_DDO_TEXT_SIZE:
                logger.error(f'ddo test is to large {len(ddo_text)}')
            tx_hash = self.call('registerDID', (did_id, ddo_text), account)
        return tx_hash

    def get_block_number(self, did: str) -> int:
        block_number = None
        did_id = did_to_id(did)
        if did_id:
            did_id = self._web3.toBytes(hexstr=did_id)
            block_number = self.call('getBlockNumberUpdated', did_id)
        return block_number

    def get_value(self, did: str) -> str:
        block_number = self.get_block_number(did)
        if block_number:
            did_id = self._web3.toBytes(hexstr=did_to_id(did))
            event_filter = self.create_event_filter(
                'DIDRegistered',
                None,
                from_block=block_number,
                argument_filters={'_did': did_id}
            )

            if event_filter:
                for event_log in event_filter.get_all_entries():
                    event_args = event_log.args
                    return event_args['_value']
        return None
