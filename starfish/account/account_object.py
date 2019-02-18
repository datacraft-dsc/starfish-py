
"""
    Basic squid object
"""

class AccountObject():
    def __init__(self, ocean):
        """init the the Account Object Base with the ocean instance"""
        self._ocean = ocean

    @property
    def ocean(self):
        return self._ocean
