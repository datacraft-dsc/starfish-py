
"""
    Basic agent object
"""

class Agent():
    """

    Base agent class

    :param ocean: Ocean object that is used by the Agent class
    :type ocean: :class:`.Ocean`
    """
    def __init__(self, ocean):
        """init the the Ocean Object Base with the ocean instance"""
        self._ocean = ocean


    @property
    def ocean(self):
        """
        :return: Ocean object
        :type: :class:`.Ocean`
        """
        return self._ocean
