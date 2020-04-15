"""

    Test tool asset

"""


from starfish.tool.command.asset_command import AssetCommand
from starfish.tool.command.asset_store_command import AssetStoreCommand


def test_tool_asset(sub_parser):
    asset = AssetCommand()
    parser = asset.create_parser(sub_parser)
    assert(parser)

def test_tool_asset_wait(parser, sub_parser):
    asset = AssetCommand()
    asset_parser = asset.create_parser(sub_parser)
    assert(asset_parser)

    store = AssetStoreCommand()
    store_parser = store.create_parser(asset_parser)
    assert(store_parser)
    args = parser.parse_args(['asset', 'store', 'agent_url_did', 'filename'])
    assert(args)
