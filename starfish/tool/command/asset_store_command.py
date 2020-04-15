"""

    Command 'Asset Store'

"""
import os

from starfish.agent import (
    AgentManager,
    RemoteAgent
)
from starfish.asset import DataAsset
from .command_base import CommandBase


DEFAULT_ASSET_NAME = 'starfish_asset'


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
            '-n',
            '--name',
            default=DEFAULT_ASSET_NAME,
            help='Asset name. Default: {DEFAULT_ASSET_NAME}'
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

        if not os.path.exists(args.filename):
            output.add_line(f'cannot find file {args.filename}')
            return

        network = self.get_network(args.url)

        result = AgentManager.resolve_agent(args.agent, network, args.username, args.password)
        if not result:
            output.add_line(f'cannot resolve asset {args.asset}')
            return

        authentication = None
        if args.username or args.password:
            authentication = {
                'username': args.username,
                'password': args.password
            }

        agent = RemoteAgent(network, result['ddo_text'], authentication=authentication)
        asset = DataAsset.create_from_file(args.name, args.filename)
        asset = agent.register_asset(asset)
        agent.upload_asset(asset)
        output.add_line(f'stored asset {asset.did}')
        output.set_value('asset_did', asset.did)
