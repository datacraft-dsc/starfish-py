"""
    starfish-ddo-registry contract

"""

from starfish.network.convex.contract.contract_base import ContractBase
from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.convex.convex_network import ConvexNetwork
from starfish.types import AccountAddress


class ProvenanceContract(ContractBase):

    def __init__(self, convex: ConvexNetwork):
        ContractBase.__init__(self, convex, 'starfish-provenance', '0.0.1')

        self._source = f'''
            (def provenance [])
            (defn version [] "{self.version}")
            (defn assert-asset-id [value]
                (when-not (and (blob? value) (== 32 (count (blob value)))) (fail "INVALID" "invalid asset-id"))
            )
            (defn assert-address [value]
                (when-not (address? (address value)) (fail "INVALID" "invalid address"))
            )
            (defn register [asset-id]
                (assert-asset-id asset-id)
                (let [record {{:owner *caller* :timestamp *timestamp* :asset-id (blob asset-id)}}]
                    (def provenance (conj provenance record))
                    record
                )
            )
            (defn event-list [asset-id]
                (assert-asset-id asset-id)
                (mapcat (fn [record] (when (= (blob asset-id) (record :asset-id)) [record])) provenance)
            )
            (defn event-owner [owner-id]
                (assert-address owner-id)
                (mapcat (fn [record] (when (= (address owner-id) (record :owner)) [record])) provenance)
            )
            (defn event-timestamp [time-from time-to]
                (mapcat
                    (fn [record]
                        (when
                            (and
                                (<= time-from (record :timestamp))
                                (>= time-to (record :timestamp))
                            )
                        [record] )
                    )
                provenance)
            )
            (export event-list event-owner event-timestamp register version)

'''

    def register_did(self, asset_id: str, account: ConvexAccount):
        command = f'(call {self.address} (register {asset_id}))'
        result = self._convex.send(command, account)
        if result and 'value' in result:
            return result['value']
        return result

    def event_list(self, asset_id: str, account_address: AccountAddress):
        command = f'(call {self.address} (event_list {asset_id}))'
        if isinstance(account_address, str):
            address = account_address
        else:
            address = account_address.address
        result = self._convex.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result
