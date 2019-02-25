
"""
    Basic agent object
"""

class Agent():
    def __init__(self, ocean):
        """init the the Ocean Object Base with the ocean instance"""
        self._ocean = ocean


    @property
    def ocean(self):
        """
        :return: Ocean object
        """
        return self._ocean
