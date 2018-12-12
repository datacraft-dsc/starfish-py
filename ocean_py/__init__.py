"""
    Ocean-py module init


    Return the global logger, hopefully you have called ocean-py.logging.setup_logging, before using this
"""


__author__ = """OceanProtocol"""
__version__ = '0.0.1'


import logging

logger = logging.getLogger(__name__)
