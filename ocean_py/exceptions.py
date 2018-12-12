# Exceptions for squid-py


# Raised when an invalid address is passed to the contract loader
class OceanInvalidContractAddress(Exception):
    pass

# raised on command line errors
class OceanCommandLineError(Exception):
    pass
