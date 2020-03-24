"""

    Agent Manager, to load and resolve remote agents

"""
from starfish.agent.remote_agent import RemoteAgent
from starfish.ddo import DDO


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

            ddo = RemoteAgent.resolve_network_ddo(self._network, item.get('did', None))
            if ddo is None:
                authentication_access = None
                if item.get('username', None):
                    authentication_access = {
                        'username': item.get('username', None),
                        'password': item.get('password', None)
                    }
                ddo = RemoteAgent.resolve_url_ddo(item.get('url', None), authentication_access)

            self._items[name]['ddo'] = ddo
        return self._items[name]['ddo']

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

        if ddo_text:
            ddo = DDO(json_text=ddo_text)
            if ddo:
                authentication_access = None
                item = self._items[name]
                if item.get('username', None):
                    authentication_access = {
                        'username': item.get('username', None),
                        'password': item.get('password', None)
                    }
                agent = RemoteAgent(self._network, ddo, authentication_access)
        return agent

    @property
    def items(self):
        return self._items
