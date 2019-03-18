"""

Surfer Agent class to provide basic functionality for Ocean Agents

"""

import secrets
import re
import json

# from squid_py.did import id_to_did

from starfish.account import Account
from starfish.agent import Agent
# from starfish.listing import Listing
from starfish.asset import Asset
from starfish.utils.did import did_parse


class SurferAgent(Agent):
    """

    Surfer Agent class allows to register, list, purchase and consume assets.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`

    """

    def __init__(self, ocean, *args, **kwargs):
        """init a standard ocean object"""
        Agent.__init__(self, ocean)

    def register_asset(self, asset):
        """

        Register a memory asset with the ocean network (surfer)
        FIXME BELOW

        :param dict metadata: metadata dictionary to store for this asset.
        :param account: Ocean account to use to register this asset.
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        For example::

            metadata = json.loads('my_metadata')
            # get your publisher account
            account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
            agent = SurferAgent(ocean)
            listing = agent.register_asset(metadata, account)

            if listing:
                print(f'registered my listing asset for sale with the did {listing.did}')

        """

        # NOTE: use _http_client as per tests/helpers/koi_client.py
        # initialized with https://docs.python.org/3/library/http.client.html
        # and surfer config using http://localhost:8080
        # Consider ocean.registerLocalDID(surferDID,ddoString);
        # as per src/test/java/sg/dex/starfish/samples/SurferConfig.java

        # TODO register asset metadata
        # http://localhost:8080/api-docs/index.html#!/Meta_API/post_api_v1_meta_data
        # curl $args --header 'Content-Type: application/json' \
        #   --header 'Accept: application/json' \
        #   -o "$assetidfile" -d @"$metadatafile" $url/api/v1/meta/data \
        # asset_id = contents of assetidfile without quotes

        # TODO register asset
        # http://localhost:8080/api-docs/index.html#!/Storage_API/post_api_v1_assets_id
        # curl $args --header 'Accept: application/json' \
        #   --form file=@"$asset" $url/api/v1/assets/$assetid ; then
        # WHERE $asset is asset.data, $assetid = asset_id

        return None
