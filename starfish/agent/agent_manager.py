"""

    Agent Manager, to load and resolve remote agents

"""
import logging
from typing import Dict

from starfish.agent.remote_agent import RemoteAgent
from starfish.ddo import create_ddo_object
from starfish.ddo.ddo import DDO
from starfish.network import Network
from starfish.types import (
    AgentItem,
    Authentication,
    TRemoteAgent
)
from starfish.utils.did import (
    did_to_id,
    id_to_did
)

logger = logging.getLogger(__name__)


class AgentManager:
    def __init__(self, network: Network) -> None:
        self._network = network
        self._items = {}
        self._default_name = None

    def add(
        self,
        name: [str, dict],
        url: str = None,
        did: str = None,
        authentication: Authentication = None,
        is_default: bool = None
    ) -> None:
        """

        Add a remote agent details to the list of remote agents managed by this class.

        :param str name: name of the remote agent
        :param str,dict url: url of the remote agent, or a dict if passing a dict of items
        :param str did: DID of the agent
        :param dict authentication: Access details to pass to the agent

        """
        if url and isinstance(url, dict):
            item = url
            if 'username' in item or 'token' in item:
                authentication = {
                    'username': item.get('username', None),
                    'password': item.get('password', None),
                    'token': item.get('token', None)
                }
                item['authentication'] = authentication
        else:
            item = {
                'url': url,
                'did': did,
                'authentication': authentication,
            }
        if item['url'] is None and item['did'] is None:
            raise ValueError('You must provide at least an URL or DID for the remote agent')

        # if the is_default value is set to True, then make this the default agent
        if is_default:
            self._default_name = is_default

        # if _default_name is not assigned, then assign it to the first name
        if self._default_name is None:
            self._default_name = name

        self._items[name] = item

    def resolve_ddo(self, name: str) -> str:
        """

        Tries to resolve the remote agent to a ddo using it's provided URL or DID.

        :param str name: Name of the remote agent that was added to the managed list.
        :return dict: DDO text or None for the remote agent

        """

        if name not in self._items:
            raise ValueError(f'remote agent {name} not found in list')

        item = self._items[name]
        if item.get('ddo_text', None) is None:

            ddo_text = self._network.resolve_did(item.get('did', None))
            if ddo_text is None:
                authentication = item.get('authentication', None)
                ddo_text = RemoteAgent.resolve_url(item.get('url', None), authentication=authentication)

            self._items[name]['ddo_text'] = ddo_text
            self._items[name]['ddo'] = create_ddo_object(ddo_text)
        return self._items[name]['ddo_text']

    def load_agent(self, asset_agent_did_name: str) -> TRemoteAgent:
        """

        Resolves and gets a valid remote agent for a given asset_did, agent_did or agent name

        :param str asset_agent_did_name:  Can be an asset_did, agent_did or name of the agent held by this object

        :return RemoteAgent: Object or None if none found

        """

        agent = None
        ddo_text = None

        # test for name in the agent list
        if asset_agent_did_name in self._items:
            logger.debug(f'found {asset_agent_did_name} in the list of agents')
            ddo_text = self.resolve_ddo(asset_agent_did_name)
        else:
            # find in list of did's
            # strip away the asset part of the id
            did_id = did_to_id(asset_agent_did_name)
            did = id_to_did(did_id)
            logger.debug(f'stripped possible did {asset_agent_did_name} to {did}')
            item = self.get_item_from_did(did)
            if item:
                logger.debug(f'found {did} in list of resolved items')
                ddo_text = item['ddo_text']
            else:
                # if it's a agent_did or asset_did
                ddo_text = self._network.resolve_did(did)
                if ddo_text:
                    logger.debug(f'resolved {did} from network')

        if ddo_text:
            ddo = DDO(json_text=ddo_text)
            authentication = None

            item = self.get_item_from_did(ddo.did)
            if item:
                authentication = item.get('authentication', None)
            agent = RemoteAgent(ddo_text, authentication=authentication)
        return agent

    def get_item_from_did(self, find_did: str) -> AgentItem:
        for name, item in self._items.items():
            did = None
            if 'ddo' in item:
                did = item['ddo'].did
            elif 'ddo_text' in item:
                ddo = create_ddo_object(item['ddo_text'])
                did = ddo.did
            if did and did == find_did:
                return item
        return None

    @property
    def default_name(self) -> str:
        return self._default_name

    @default_name.setter
    def default_name(self, value: str) -> None:
        self._default_name = value

    @property
    def items(self) -> Dict[str, AgentItem]:
        return self._items
