"""

    Exceptions for starfish-py

"""


class OceanInvalidContractAddress(Exception):
    """  Raised when an invalid address is passed to the contract loader """

class OceanCommandLineError(Exception):
    """ raised on command line errors """

class StarfishPurchaseError(Exception):
    """ Raised when a purchase events have failed to complete """

class StarfishAssetNotFound(Exception):
    """ Raised when an asset is not found """

class StarfishAssetInvalid(Exception):
    """ Raised when a downloaded asset is not valid or has been changed """
