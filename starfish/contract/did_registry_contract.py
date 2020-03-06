"""

    DIDRegistry Contract

"""

import logging


from starfish.contract.contract_base import ContractBase
from starfish.utils.did import did_to_id

logger = logging.getLogger(__name__)

CONTRACT_NAME = 'DIDRegistry'

MAX_DDO_TEXT_SIZE = 2048

class DIDRegistryContract(ContractBase):
    """

    Class representing the DIDRegistry contract.

    """

    def __init__(self):
        ContractBase.__init__(self, CONTRACT_NAME)


    def register(self, account, did, ddo_text):
        did_id = self._web3.toBytes(hexstr=did_to_id(did))
        if len(ddo_text) > MAX_DDO_TEXT_SIZE:
            logger.error(f'ddo test is to large {len(ddo_text)}')
        tx_hash = self.call('registerDID', (did_id, ddo_text), account)
        return tx_hash

    def get_block_number_for_did(self, did):
        did_id = self._web3.toBytes(hexstr=did_to_id(did))
        block_number = self.call('getBlockNumberUpdated', did_id)
        return block_number

    def get_value(self, did):
        block_number = self.get_block_number_for_did(did)
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
