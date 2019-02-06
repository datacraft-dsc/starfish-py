"""
    Agent class to provide basic functionality for all Ocean Agents
"""

class Agent():

    def __init__(self, ocean, **kwargs):
        """init a standard ocean agent"""
        self._ocean = ocean
        self._did = kwargs.get('did')

    def register(self, service_name, endpoint_url, account, did=None):
        """
        Register an agent on the block chain
        :param service_name: service_name to add into the DDO service field
        :param endpoint_url: url of the agent service
        :param account: Ethereum account to use to register on the block chain
        :param did: optional did to update the did with this value (if you are the account owner of the DID)

        """

        if did is None:
            # if no did then we need to create a new one
            did = id_to_did(secrets.token_hex(32))

        # create a new DDO
        ddo = DDO(did)
        # add a signature
        private_key_pem = ddo.add_signature()
        # add the service endpoint with the meta data
        ddo.add_service(service_name, endpoint_url)
        # add the static proof
        ddo.add_proof(0, private_key_pem)
        if self._register_ddo(did, ddo, account):
            return [did, ddo, private_key_pem]
        return None

    def _register_ddo(self, did, ddo, account):
        """register a ddo object on the block chain for this agent"""
        # register/update the did->ddo to the block chain
        return self._ocean.keeper.did_registry.register(did, ddo=ddo, account=account)
