"""

Agent class for Invokable Ocean Agents

"""

import logging
from starfish.operation.operation import Operation

logger = logging.getLogger('starfish.invoke_agent')

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
        return []
#        r=requests.get(self._koi_url+'operations')
#        j=json.loads(r.text)
#        self.operations=dict(zip([i['name'] for i in j],[i['did'] for i in j]))
#        return self.operations

    def get_operation(self,did):
        return Operation(self,did)

    def get_listing(self, listing_id):
        """

        Return an listing from the given listing_id.

        :param str listing_id: Id of the listing.

        :return: a registered listing given a Id of the listing
        :type: :class:`.Listing` class

        """

    def purchase(self, listing, account):
        """

        Purchase an asset using it's listing and an account.-will be supported in future

        """
        pass
