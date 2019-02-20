"""
    Asset class to handle core imutable asset and it's metadata


"""


class Asset():
    """

    :param dict metadata: metadata for the asset
    :param str did: did of the asset.

    """
    def __init__(self, metadata, did):
        """
        init an asset class
        """
        self._metadata = metadata
        self._did = did

    @property
    def did(self):
        """
        :return: the asset did
        :type: str
        """
        return self._did

    @property
    def metadata(self):
        """
        :return: The metadata for this asset
        :type: dict
        """
        return self._metadata
