"""
    Starfish-py module

    This module contains the following classes

    * :class:`Agent` The Agent wrapper class.
    * :class:`Asset` The Asset class.
    * :class:`Config` The Config data class.
    * :class:`Ocean` The main Ocean connection class.
    * :data:`logger` The logger class.
"""

__author__ = """DEX.sg"""
__version__ = '0.0.1'

import logging

logger = logging.getLogger(__name__)

from .agent import Agent
from .asset.asset import Asset
from .asset.asset_light import AssetLight
from .config import Config
from .ocean import Ocean
