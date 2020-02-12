"""
    Starfish-py module

    This module contains the following classes

    * :class:`Account` The Account class.
    * :class:`Ocean` The main Ocean connection class.
    * :data:`logger` The logger class.
"""

__author__ = """DEX.sg"""
__version__ = '0.6.5'

import logging

logger = logging.getLogger(__name__)


from starfish.ocean.ocean import Ocean
