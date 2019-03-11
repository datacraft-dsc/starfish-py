"""
    Test invoke agent

"""

import pathlib
import json
import logging
import time
from squid_py.keeper import Keeper
from squid_py.keeper.didregistry import DIDRegistry
from squid_py.accounts.account import Account
from squid_py.config_provider import ConfigProvider
from squid_py.config import Config
from squid_py.keeper.web3_provider import Web3Provider

from starfish import (
    Ocean,
    logger
)

from starfish.logging import setup_logging

setup_logging(level=logging.DEBUG)

PUBLISHER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}

def test_raw_register():
    ConfigProvider.set_config(Config(options_dict={'keeper-contracts':{'keeper.path':'artifacts','parity_url': 'http://localhost:9545'}}))
    keeper=Keeper.get_instance()
    assert keeper

    did='did:op:e115810f714d4d5082e848567e6d4fb0c124a77445de4a6492712d80e7f78714'
    keeper.did_registry.register(did,
            Web3Provider.get_web3().sha3(text=did),
            'http://google.com',
            Account(PUBLISHER_ACCOUNT['address'],password=PUBLISHER_ACCOUNT['password']))


