"""
    Asset class to handle core imutable asset and it's metadata


"""


class Asset():
    """

        :param metadata: Optional metadata for the asset
        :type metadata: dict or None

    """
    def __init__(self, did=None, metadata=None):
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
