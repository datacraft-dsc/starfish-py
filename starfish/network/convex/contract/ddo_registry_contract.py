"""
    starfish-ddo-registry contract

"""

CONTRACT_NAME='starfish-ddo-registry'
CONTRACT_VERSION = '0.0.4'

ddo_registry_contract = f"""
(def {CONTRACT_NAME}
    (deploy
        '(do
            (def registry {{}})
            (def creator *caller*)
            (defn version [] "{CONTRACT_VERSION}")
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
        )
    )
)
"""
