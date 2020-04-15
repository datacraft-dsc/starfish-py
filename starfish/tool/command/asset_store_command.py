"""

    Command 'Asset Store'

"""

from .command_base import CommandBase


class AssetStoreCommand(CommandBase):

    def __init__(self, sub_parser=None):
        self._command_list = []
        super().__init__('store', sub_parser)

    def create_parser(self, sub_parser):

        parser = sub_parser.add_parser(
            self._name,
            description='Tool to store an asset',
            help='Tool to store an asset',

        )

        return parser

    def execute(self, args, output):
        pass