"""

    Command 'Asset Store'

"""

import datetime
import os
import re
from typing import Any

from starfish.agent import RemoteAgent
from starfish.asset import DataAsset
from .command_base import CommandBase


DEFAULT_ASSET_NAME = 'starfish_asset'


class AssetStoreCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('store', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

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
            '--description',
            help='Asset metadata description'
        )

        parser.add_argument(
            '--date-created',
            help='Asset metadata dateCreated'
        )

        parser.add_argument(
            '--created-now',
            action='store_true',
            help='Asset metadata set the dateCreated field to the current local time'
        )

        parser.add_argument(
            '--author',
            help='Asset metadata author'
        )

        parser.add_argument(
            '--license',
            help='Asset metadata license'
        )

        parser.add_argument(
            '--copyright-holder',
            help='Asset metadata copyrightHolder'
        )

        parser.add_argument(
            '--in-language',
            help='Asset metadata inLanguage'
        )

        parser.add_argument(
            '--tags',
            help='Asset metadata tags (string comma seperated list)'
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

    def execute(self, args: Any, output: Any) -> None:

        if not os.path.exists(args.filename):
            output.add_line(f'cannot find file {args.filename}')
            return

        network = self.get_network(args.url)

        ddo = network.resolve_agent(args.agent, username=args.username, password=args.password)
        if not ddo:
            output.add_line(f'cannot resolve asset {args.asset}')
            return

        authentication = None
        if args.username or args.password:
            authentication = {
                'username': args.username,
                'password': args.password
            }

        agent = RemoteAgent(ddo=ddo, authentication=authentication)
        metadata = {}

        if args.description:
            metadata['description'] = args.description

        if args.created_now:
            metadata['dateCreated'] = datetime.datetime.now().isoformat()

        if args.date_created:
            metadata['dateCreated'] = args.date_created

        if args.author:
            metadata['author'] = args.author

        if args.license:
            metadata['license'] = args.license

        if args.copyright_holder:
            metadata['copyrightHolder'] = args.copyright_holder

        if args.in_language:
            metadata['inLanguage'] = args.in_language

        if args.tags:
            print('tags', args.tags)
            tag_list = re.split(r'[\s\S]+', args.tags)
            metadata['tags'] = tag_list

        if not metadata.keys():
            metadata = None

        asset = DataAsset.create_from_file(args.name, args.filename, metadata=metadata)
        asset = agent.register_asset(asset)
        agent.upload_asset(asset)
        output.add_line(f'stored asset {asset.did}')
        output.set_value('asset_did', asset.did)
