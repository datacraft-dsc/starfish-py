
"""

Trade class to hold Ocean tradeing information such as an asset id and metadata

"""

from eth_utils import remove_0x_prefix

from squid_py.did import did_to_id

from starfish import (
    Account
)

from starfish.models.squid_model import SquidModel
from starfish.utils.did import did_parse
from starfish.purchase import SquidPurchase
from starfish.listing import ListingObject

# from starfish import logger


class SquidListing(ListingObject):
    """

    The creation of an asset is normally performed by the :class:`.SquidAgent` class.

    :param agent: ocean object to use to connect to the ocean network.
    :type agent: :class:`.SquidAgent`
    :param did: Optional did of the asset.
    :type did: str or None
    :param ddo: Optional DDO to assign to this asset.
    :type ddo: dict or None

    """
    def __init__(self, agent, did=None, ddo=None):
        """init a standard ocean object"""
        ListingObject.__init__(self, agent, did)

        self._ddo = None
        if ddo:
            self._set_ddo(ddo)

        if did:
            self._id = did_to_id(did)

    def read(self):
        """

        Read the asset metadata in this case it's the DDO with the metadata
        included from the off chain metadata agent.

        :return: metadata of the asset, or None if not found in storage.
        :type: dict

        """

        model = self.agent.squid_model

        self._metadata = None
        ddo = model.read_asset(self._did)
        if ddo:
            self._set_ddo(ddo)

        # TODO: Resolve the agent endpoints for this asset.
        # The DID we can get squid to go too the blockchain, resolve the URL then get the DDO
        # from the DDO we can then decode using the SecretStore brizo url's

        return self._metadata

    def purchase(self, account):
        """

        Purchase this asset listing using the account details, return a purchased asset
        with the service_agreement_id ( purchase_id ) set.

        :param account: account to use to purchase this asset.
        :type account: :class:`.Account`

        :return: asset object that has been purchased
        :type: :class:`.Asset`

        """
        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        purchase = None
        model = self.agent.squid_model
        
        if self.ddo is None:
            self.read()
            
        service_agreement_id = model.purchase_asset(self, account)
        if service_agreement_id:
            purchase = SquidPurchase(self._agent, self, service_agreement_id)
            
        return purchase

    def _set_ddo(self, ddo):
        """

        Assign ddo values to the asset id/did and metadata properties

        """
        self._did = ddo.did
        self._id = remove_0x_prefix(did_to_id(self._did))
        self._ddo = ddo

        self._metadata = ddo.get_metadata()

    @property
    def is_empty(self):
        """

        Checks to see if this Listinng is empty.

        :return: True if this listing is empty else False.
        :type: boolean
        """
        return self._did is None
        
    @property
    def ddo(self):
        """
        :return: The ddo assigned with this asset.
        :type: dict
        """
        return self._ddo

    @staticmethod
    def is_did_valid(did):
        """
        Checks to see if the DID string is a valid DID for this type of Asset.
        This method only checks the syntax of the DID, it does not resolve the DID
        to see if it is assigned to a valid Asset.

        :param str did: DID string to check to see if it is in a valid format.

        :return: True if the DID is in the format 'did:op:xxxxx'
        :type: boolean
        """
        data = did_parse(did)
        return not data['path']
