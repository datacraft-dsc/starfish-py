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
            'agent',
            help='agent url or agent did to store the asset'
        )

        parser.add_argument(
            'filename',
            help='filename to store'
        )

        return parser

    def execute(self, args, output):
        pass
