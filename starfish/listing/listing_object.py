
"""
    Basic Listing object
"""

class ListingObject():
    """
        Create a basic ListingObject

        :param agent: agent object that created the listing.
        :type agent: :class:`.Agent` object to assign to this Listing
        :param asset: the core asset
        :type asset: :class:`.Asset` object
        :param data: data of the listing
        :type data: dict
    """
    def __init__(self, agent, asset, data):
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._asset = asset
        self._data = data

    @property
    def agent(self):
        """

        :return: Agent object that created this listing
        :type: :class:`.SquidAgent`
        """
        return self._agent

    @property
    def data(self):
        """

        :return: data of the listing
        :type: dict or None
        """
        return self._data

    @property
    def asset(self):
        """

        :return: asset held by the listing
        :type: :class:`.Asset`
        """
        return self._asset

    @property
    def is_empty(self):
        """

        Checks to see if this Listinng is empty.

        :return: True if this listing is empty else False.
        :type: boolean
        """
        return self._did is None or self._asset is None
