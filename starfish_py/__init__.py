"""
    Starfish-py module

    The main class to call is the :func:`starfish_py.ocean.Ocean` class.


"""


__author__ = """DEX.sg"""
__version__ = '0.0.1'

import logging

logger = logging.getLogger(__name__)


from .asset.asset import Asset
from .asset.asset_light import AssetLight

from .agent import Agent
from .config import Config
from .ocean import Ocean



