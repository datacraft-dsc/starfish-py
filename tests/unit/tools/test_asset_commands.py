"""

    Test tool asset

"""
import pytest

from starfish.tool.command.asset_command import AssetCommand
from starfish.tool.command.asset_store_command import AssetStoreCommand


@pytest.fixture(scope='module')
def asset_parser(sub_parser):
    asset = AssetCommand()
    asset_parser = asset.create_parser(sub_parser)
    assert(asset_parser)
    return asset_parser

def test_tool_asset(asset_parser):
    assert(asset_parser)

def test_tool_asset_store(parser, asset_parser):
    store = AssetStoreCommand()
    store_parser = store.create_parser(asset_parser)
    assert(store_parser)
    args = parser.parse_args(['asset', 'store', 'agent_url_did', 'filename'])
    assert(args)

def test_tool_asset_download(parser, asset_parser):
    store = AssetStoreCommand()
    store_parser = store.create_parser(asset_parser)
    assert(store_parser)
    args = parser.parse_args(['asset', 'download', 'asset_did'])
    assert(args)
