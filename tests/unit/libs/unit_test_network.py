
from starfish.network.ethereum_network import EthereumNetwork

class UnitTestNetwork(EthereumNetwork):

    def __init__(self, url):
        self._url = url

