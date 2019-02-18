"""
    Starfish-py module

    This module contains the following classes

    * :class:`Account` The Account class.
    * :class:`Ocean` The main Ocean connection class.
    * :data:`logger` The logger class.
"""

__author__ = """DEX.sg"""
__version__ = '0.0.1'

import logging

logger = logging.getLogger(__name__)


from starfish.account.account import Account
from starfish.ocean.ocean import Ocean


