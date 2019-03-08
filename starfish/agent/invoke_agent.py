"""

Agent class to provide basic functionality for all Ocean Agents

#returns a Listing object.
listing=agent.get_listing(did)
#returns operation

operation=listing.purchase(XX)
#invoke operation
operation.invoke(XX)
"""



import logging
import json
from starfish.account import Account
from starfish.agent import Agent
from starfish.listing import Listing
from starfish.asset import SquidAsset
from starfish.purchase import Purchase
from starfish.operation.operation import Operation
import sys,traceback
logger = logging.getLogger('ocean')
import requests

class InvokeAgent:
    """

    Invoke Agent class allows get a list of operations and invoke them.

    """
    
    def __init__(self, **kwargs):
        """init a standard ocean object"""

        self._koi_url = kwargs.get('koi_url', 'http://localhost:8031/api/v1/brizo/services/')

        r=requests.get(self._koi_url+'operations')
        j=json.loads(r.text)
        self.operations=dict(zip([i['name'] for i in j],[i['did'] for i in j]))

    def get_operations(self):
        """ 
        returns a list of operations and their associated DIDs.
        """
        return self.operations  
    
    def get_operation(self,did):
        return Operation(self,did)        

    def get_listing(self, did):
        """

        Return an listing on the listing's DID.

        :param str did: DID of the listing.

        :return: a registered asset given a DID of the asset
        :type: :class:`.SquidAsset` class

        """
        pass 


    def purchase(self, listing, account):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        """
        purchase = None
        return purchase

    def invoke_operation(self,listing, purchase_id, account, payload):
        """
        Invoke the operation

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param str purchase_id: purchase id that was used to purchase the asset.
        :param account: Ocean account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str payload: params required for the operation

        :return: True if the operation was invoked
        :type: boolean

        """
        logger.info(f'calling invoke in squid_agent.py with payload: {payload}')

