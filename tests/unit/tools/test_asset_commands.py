"""

    Test tool asset

"""
import argparse


from starfish.tool.command.asset_command import AssetCommand
from starfish.tool.command.asset_store_command import AssetStoreCommand


def get_sub_parser():
    parser = argparse.ArgumentParser(description='Starfish Tools')

    sub_parser = parser.add_subparsers(
        title='Starfish command',
        description='Tool command',
        help='Tool command',
        dest='command'
    )
    return sub_parser

def test_tool_asset():
    account = AssetCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_asset_wait():
    account = AssetStoreCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)
