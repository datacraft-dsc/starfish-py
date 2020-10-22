
from starfish.network.ethereum import EthereumNetwork

class UnitTestNetwork(EthereumNetwork):

    def __init__(self, url):
        self._url = url

