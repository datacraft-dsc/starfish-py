"""
    Ocean-py module init
    
"""


__author__ = """OceanProtocol"""
__version__ = '0.0.1'


import logging

""" Return the global logger, hopefully you have called ocean-py.logging.setup_logging, before using this """
logger = logging.getLogger(__name__)
