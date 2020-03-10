
from starfish.d_network import DNetwork

class UnitTestNetwork(DNetwork):

    def __init__(self):
        pass

    def connect(self, url):
        self._url = url
