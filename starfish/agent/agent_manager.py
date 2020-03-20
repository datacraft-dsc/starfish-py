"""

    Agent Manager, to load and resolve remote agents

"""

from starfish.agent.remote_agent import RemoteAgent
from starfish.ddo import DDO
from starfish.middleware.surfer_agent_adapter import SurferAgentAdapter


class AgentManager:
    def __init__(self, network):
        self._network = network
        self._items = {}

    def add(self, name, url=None, did=None, username=None, password=None):
        """

        Add a remote agent details to the list of remote agents managed by this class.

        :param str name: name of the remote agent
        :param str,dict url: url of the remote agent, or a dict if passing a dict of items
        :param str did: DID of the agent
        :param str username: Username access to the remote agent
        :param str password: Password access to the remote agent


        """
        if url and isinstance(url, dict):
            item = url
        else:
            item = {
                'url': url,
                'did': did,
                'username': username,
                'password': password
            }
        if item['url'] is None and item['did'] is None:
            raise ValueError('You must provide at least an URL or DID for the remote agent')
        self._items[name] = item

    def get_ddo(self, name):
        """

        Tries to resolve the remote agent to a ddo using it's provided URL or DID.

        :param str name: Name of the remote agent added to the managed list.
        :return dict: DDO or None for the remote agent

        """

        if name not in self._items:
            raise ValueError(f'remote agent {name} not found in list')

        item = self._items[name]
        if item.get('ddo', None) is None:
            ddo = self.get_network_ddo(item.get('did', None))
            if ddo is None:
                ddo = self.get_url_ddo(item.get('url', None), item.get('username', None), item.get('password', None))

            self._items[name]['ddo'] = ddo
        return self._items[name]['ddo']

    def get_network_ddo(self, did):
        """

        Resolves the remote agent via the dnetwork using it's did to get the agent DDO

        :param str did: DID of the remote agent to resolve and get DDO
        :return dict: DDO or None if not found in the network

        """

        ddo = None
        if did:
            ddo = self._network.resolve_did(did)
        return ddo

    def get_url_ddo(self, url, username=None, password=None):
        """

        Resolves the remote agent ddo using the url of the agent

        :param str url: url of the remote agent
        :param str username: optional username for access to the remote agent
        :param str password: optional password for access to the remote agent
        :return dict: DDO or None if not found
        """

        ddo = None
        if url:
            adapter = SurferAgentAdapter(self._network)
            headers = None
            if username:
                token_url = f'{url}/api/v1/auth/token'
                authorization = adapter.get_authorization_token(username, password, token_url)
                headers = {
                    'Authorization': f'token {authorization}'
                }

            ddo = adapter.get_ddo(url, headers)
        return ddo

    def get_remote_agent(self, name):
        """

        Resolves and gets a valid remote agent for a given asset_did, agent_did or agent name

        :param str name: Name can be an asset_did, agent_did or name of the agent held by this object

        :return RemoteAgent: Object or None if none found

        """
        agent = None
        ddo_text = None
        # test for name in the agent list
        if name in self._items:
            ddo_text = self.get_ddo(name)

        # test if the name is an agent_did or asset_did
        if name:
            ddo_text = self.get_network_ddo(name)

        if ddo_text:
            ddo = DDO(json_text=ddo_text)
            if ddo:
                options = None
                agent = RemoteAgent(self._network, ddo.did, ddo, options)
        return agent

    @property
    def items(self):
        return self._items
