"""

    Command 'Asset Store'

"""
from typing import Any

from starfish.agent import RemoteAgent
from .command_base import CommandBase


class AssetDownloadCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('download', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Tool to download an asset',
            help='Tool to download an asset',
        )

        parser.add_argument(
            '-u',
            '--username',
            help='Optional username to access the agent'
        )

        parser.add_argument(
            '-p',
            '--password',
            help='Optional password to access the agent'
        )

        parser.add_argument(
            'asset_did',
            help='asset did of the asset to download'
        )

        parser.add_argument(
            'filename',
            nargs='?',
            help='filename to download. Defaults: to the "<asset_did>.dat" '
        )

        return parser

    def execute(self, args: Any, output: Any) -> None:

        network = self.get_network(args.url)

        ddo = network.resolve_agent(args.asset_did, username=args.username, password=args.password)
        if not ddo:
            output.add_line(f'cannot resolve asset {args.asset_did}')
            return

        authentication = None
        if args.username or args.password:
            authentication = {
                'username': args.username,
                'password': args.password
            }

        agent = RemoteAgent(ddo=ddo, authentication=authentication)
        asset = agent.download_asset(args.asset_did)
        asset_filename = args.filename
        if asset_filename is None:
            asset_filename = f'{asset.id}.dat'

        asset.save_to_file(asset_filename)
        output.add_line(f'saved asset {asset_filename}')
        output.add_line(f'asset metadata {asset.metadata}')
        output.set_value('asset_did', asset.did)
        output.set_value('filename', asset_filename)
        output.set_value('metadata', asset.metadata)
