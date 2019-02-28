"""
    Squid Asset 
"""

from starfish.asset import Asset

class SquidAsset(Asset):
    def __init__(self, metadata, did=None):        
        Asset.__init__(self, metadata, did)

        
