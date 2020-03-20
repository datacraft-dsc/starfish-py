"""

    Agent Manager, to load and resolve remote agents

"""

from starfish.agent import RemoteAgent


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
            options = None
            if username:
                options = {
                    'authorization': {
                        'username': username,
                        'password': password
                    }
                }
            agent = RemoteAgent(self._network, options)
            adapter = agent._get_adapter()
            ddo = adapter.get_ddo(url)
        return ddo

    @property
    def items(self):
        return self._items
