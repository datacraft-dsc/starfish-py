
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


    def purchase_wait_for_completion(self, purchase_id, timeoutSeconds):
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        return True

    @property
    def ocean(self):
        """
        :return: Ocean object
        :type: :class:`.Ocean`
        """
        return self._ocean
