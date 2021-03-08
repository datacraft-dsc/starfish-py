"""
    Metadata class to handle asset metadata.


"""

# from starfish import logger


class Metadata():
    """

    :param agent: agent object to used to create
    :type agent: :class:`.AgentObject`
    :param metadata: Metadata.
    :type metadata: dict

    """

    def __init__(self, name=None, asset_type=None, **kwargs):
        """
        init the metadata class
        """

        self._valid_fields = [
            'name', 'type', 'description', 'dateCreated',
            'author', 'license', 'copyrightHolder', 'links', 'inLanguage',
            'tags', 'additionalInformation', 'files'
        ]

        self._data = {}

        if isinstance(name, dict):
            for name_value, value in name.items():
                self.__setitem__(name_value, value)
        elif isinstance(name, str):
            self.name = name
        else:
            raise ValueError('You need to pass the meta name as a string or dict')

        self.asset_type = asset_type

    def __setitem__(self, name, value):
        if name in self._valid_fields:
            self._data[name] = value

    def __getitem__(self, name):
        if name in self._data:
            return self._data[name]
        return None
