"""

 Utility class to get a ddo, did pair
"""
def get_ddo(config):
    surfer_url=config.surfer_url

    did="did:ocn:950d6a6111abf7acef5d85b3e6733846a8a01baa7b602a2e091accab69d980df"

    ddo= { "service": [{ "serviceEndpoint": surfer_url+'/api/v1/meta/data', "type": "Ocean.Meta.v1" }, 
                { "serviceEndpoint": surfer_url+"/api/v1/assets", "type": "Ocean.Storage.v1" }, 
                { "serviceEndpoint": surfer_url+"/api/v1/invoke", "type": "Ocean.Invoke.v1" }, 
                { "serviceEndpoint": surfer_url+"/api/v1/market", "type": "Ocean.Market.v1" }]}
    return did, ddo
