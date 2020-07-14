"""

    Command 'Asset'

"""
from typing import Any

from .asset_download_command import AssetDownloadCommand
from .asset_store_command import AssetStoreCommand
from .command_base import CommandBase
from .help_command import HelpCommand


class AssetCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('asset', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Tool tasks for assets',
            help='Tasks to perform on and with assets',

        )
        asset_parser = parser.add_subparsers(
            title='Asset sub command',
            description='Asset sub command',
            help='Asset sub command',
            dest='asset_command'
        )

        self._command_list = [
            AssetDownloadCommand(asset_parser),
            AssetStoreCommand(asset_parser),
            HelpCommand(asset_parser, self)
        ]
        return asset_parser

    def execute(self, args: Any, output: Any) -> Any:
        return self.process_sub_command(args, output, args.asset_command)
