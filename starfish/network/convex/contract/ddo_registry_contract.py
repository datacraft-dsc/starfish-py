"""
    starfish-ddo-registry contract

"""

from starfish.network.convex.contract.contract_base import ContractBase
from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.convex.convex_network import ConvexNetwork
from starfish.types import AccountAddress


class DDORegistryContract(ContractBase):

    def __init__(self, convex: ConvexNetwork):
        ContractBase.__init__(self, convex, 'starfish-ddo-registry', '0.0.4')

        self._source = f'''
            (def registry {{}})
            (def creator *caller*)
            (defn version [] "{self.version}")
            (defn get-register [did] (get registry did) )
            (defn set-register [did owner-address ddo]
                (let [register-record {{:owner owner-address :ddo ddo}}]
                    (def registry (assoc registry did register-record))
                )
            )
            (defn delete-register [did] (def registry (dissoc registry did)) )
            (defn assert-owner [did]
                (when-not (owner? did) (fail "NOT-OWNER" "not owner"))
            )
            (defn assert-address [value]
                (when-not (address? (address value)) (fail "INVALID" "invalid address"))
            )
            (defn assert-did [value]
                (when-not (and (blob? value) (== 32 (count (blob value)))) (fail "INVALID" "invalid DID"))
            )
            (defn resolve? [did]
                (assert-did did)
                (boolean (get-register did))
            )
            (defn resolve [did]
                (assert-did did)
                (when-let [register-record (get-register did)] (register-record :ddo))
            )
            (defn owner [did]
                (assert-did did)
                (when-let [register-record (get-register did)] (register-record :owner))
            )
            (defn owner? [did] (= (owner did) *caller*) )
            (defn register [did ddo]
                (assert-did did)
                (when (resolve? did) (assert-owner did))
                (set-register did *caller* ddo)
                did
            )
            (defn unregister [did]
                (when (resolve? did)
                    (assert-owner did)
                    (delete-register did)
                    did
                )
            )
            (defn transfer [did to-account]
                (when (resolve? did)
                    (assert-owner did)
                    (assert-address to-account)
                    (set-register did (address to-account) (resolve did))
                    [did (address to-account)]
                )
            )
            (defn owner-list [the-owner]
                (assert-address the-owner)
                (mapcat (fn [v] (when (= (address the-owner) (get (last v) :owner)) [(first v)])) registry)
            )
            (export resolve resolve? register unregister owner owner? owner-list transfer version)
        '''

    def register_did(self, did: str, ddo_text: str, account: ConvexAccount):
        command = f'(call {self.address} (register {did} "{ddo_text}"))'
        result = self._convex.send(command, account)
        if result and 'value' in result:
            return result['value']
        return result

    def resolve(self, did: str, account_address: AccountAddress):
        command = f'(call {self.address} (resolve {did}))'
        if isinstance(account_address, str):
            address = account_address
        else:
            address = account_address.address
        result = self._convex.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result

    def owner(self, did: str,  account_address: AccountAddress):
        command = f'(call {self.address} (owner {did}))'
        if isinstance(account_address, str):
            address = account_address
        else:
            address = account_address.address
        result = self._convex.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result
