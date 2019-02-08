"""

Asset class to hold Ocean asset information such as an asset id and metadata

"""

from eth_utils import remove_0x_prefix

from squid_py.did import did_to_id
from squid_py import DDO

from starfish_py.asset.asset_base import AssetBase
from starfish_py.models.squid_model import SquidModel

from starfish_py.utils.did import did_parse


# from starfish_py import logger


class Asset(AssetBase):
    """
    The creation of an asset is normally performed by the :func:`starfish_py.ocean.Ocean' class.

    :param ocean: ocean object to use to connect to the ocean network.
    :param did: Optional did of the asset.
    :param purchase_id: Optional purchase_id to assign to this asset.
    :param asset: Optional asset to copy from.
    :param ddo: Optional DDO to assign to this asset.

    """
    def __init__(self, ocean, did=None, purchase_id=None, asset=None, ddo=None):
        """
        init an asset class with the following:
        """
        AssetBase.__init__(self, ocean, did=did, asset=asset)
        self._ddo = None
        self._purchase_id = None

        # copy from another asset
        if asset:
            self._ddo = asset.ddo
            self._purchase_id = asset.purchase_id

        if purchase_id:
            self._purchase_id = purchase_id

        if did:
            self._id = did_to_id(did)

    def register(self, metadata, account):
        """

        Register on chain asset

        :param metadata: dict of the metadata to use for registration
        :param account: Ocean account to use too register this asset

        :return: The new asset's metadata
        """

        model = SquidModel(self._ocean)

        self._metadata = None
        ddo = model.register_asset(metadata, account)
        if ddo:
            self._set_ddo(ddo)

        return self._metadata

    def read(self):
        """

        Read the asset metadata in this case it's the DDO with the metadata
        included from the off chain metadata agent.

        :return: metadata of the asset, or None if not found in storage.

        """

        model = SquidModel(self._ocean)

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

        Purchase this asset using the account details, return a copy of this asset
        with the service_agreement_id ( purchase_id ) set.

        :return: asset object that has been purchased
        """
        model = SquidModel(self._ocean)
        service_agreement_id = model.purchase_asset(self, account)
        if service_agreement_id:
            purchase_asset = self.copy()
            purchase_asset.set_purchase_id(service_agreement_id)
            return purchase_asset
        return None


    def is_purchase_valid(self, account):
        """

        Test to see if this purchased asset can be accessed and is valid.

        :return: boolean value if this asset has been purchased
        """
        print(self._purchase_id)
        if not self.is_purchased:
            return False

        model = SquidModel(self._ocean)
        return model.is_access_granted_for_asset(self, self._purchase_id, account)

    def consume(self, account):
        """

        Consume a purchased asset. This call will try to download the asset data
        that you have already called using the :func:`purchase` method.

        You can call the :func:`is_purchased` property before hand to check that you
        have already purchased this asset.

        :return: data returned from the asset , or False
        """
        if not self.is_purchased:
            return False

        model = SquidModel(self._ocean)
        return model.consume_asset(self, self._purchase_id, account)

    def set_purchase_id(self, service_agreement_id):
        """

        Set the purchase id or 'service_agreement_id'

        """
        self._purchase_id = service_agreement_id

    def copy(self):
        """

        Copy this asset and return a duplicate.

        :return: copy of this asset.
        """
        return Asset(self._ocean, asset=self)

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

        Checks to see if this Asset is empty.

        :return: True if this asset is empty else False.
        """
        return  self._id is None

    @property
    def ddo(self):
        """
        :return: The ddo assigned with this asset.
        """
        return self._ddo

    @property
    def is_purchased(self):
        """
        :return: True if this asset is a purchased asset.
        """
        return not self._purchase_id is None

    @property
    def purchase_id(self):
        """
        :return: The purchase id for this asset, if not purchased then return None.
        """
        return self._purchase_id

    @staticmethod
    def is_did_valid(did):
        """
        :return: True if the DID is in the format 'did:op:xxxxx'
        """
        data = did_parse(did)
        return not data['path']
