"""

Agent class for Invokable Ocean Agents

"""


import logging
import json
from starfish.operation.operation import Operation
logger = logging.getLogger('ocean')
import requests

class InvokeAgent:
    """

    Invoke Agent class allows get a list of operations and invoke them.

    """
    def __init__(self, **kwargs):
        """init a standard ocean object"""

        self._koi_url = kwargs.get('koi_url', 'http://localhost:8031/api/v1/brizo/services/')

    def get_operations(self):
        """
        returns a list of operations and their associated DIDs.
        """
        r=requests.get(self._koi_url+'operations')
        j=json.loads(r.text)
        self.operations=dict(zip([i['name'] for i in j],[i['did'] for i in j]))
        return self.operations

    def get_operation(self,did):
        return Operation(self,did)

    def get_listing(self, did):
        """

        Return an listing on the listing's DID-will be supported in future.

        """
        pass


    def purchase(self, listing, account):
        """

        Purchase an asset using it's listing and an account.-will be supported in future

        """
        pass
