"""

    Agent Manager


"""

from starfish.agent import RemoteAgent
from starfish.agent_manager.agent_access import AgentAccess
from starfish.network.ddo import DDO

LOCAL_AGENT_NAME = '_local_agent'


class AgentManager:

    def __init__(self, network=None):
        """
        Create an agent manager object to resolve agents and keep a list of knwon agents.
        If the list of known agents only have a url, then the agent manager will try
        to resolve the url's to DID's, using the api call to obtain the DDO from the
        remote agents.

        """
        self._agent_access_items = {}
        self._local_name = LOCAL_AGENT_NAME
        self._network = network

    def register_agents(self, agents, http_client=None):
        """
        Register a dict of agents and their url/did and access information.
        This allows the agent manager to resolve 'agent names'.
        So that you can pass a given name for the agent

        :param dict agents: Dict of agents that can be stored in the agent manager.
        :param object http_client: HTTP client to make the requests to resolve and load the agent

        The agents structure can have the following optional fields

        .. code-block:: yaml

            agent_name:
              url: URL of agent
              ddo: ddo object of agent
              ddo_text: ddo text of agent ( ddo.as_text )
              did: did of the agent
              authentication:
                username: username to acces the agent api
                password: password to acces the agent api
                token: token to access the agent api
              username: username to acces the agent api
              password: password to acces the agent api
              token: token to access the agent api

            # example config, both types of authentication will work

            surfer:
              url: http://localhost:3030
              username: Aladdin
              password: OpenSesame

            invokable:
              url: http://localhost:9090
              authentication:
                username: Aladdin
                password: OpenSesame


        """
        if not isinstance(agents, dict):
            raise TypeError('agents parameter must be a type dict')

        for name, agent in agents.items():
            self.register_agent(
                name,
                ddo_text=agent.get('ddo_text', None),
                ddo=agent.get('ddo', None),
                did=agent.get('did', None),
                url=agent.get('url', None),
                authentication=agent.get('authentication', None),
                username=agent.get('username', None),
                password=agent.get('password', None),
                token=agent.get('token', None),
                http_client=http_client
            )

    def register_agent(
        self,
        name,
        ddo_text=None,
        ddo=None,
        did=None,
        url=None,
        authentication=None,
        username=None,
        password=None,
        token=None,
        http_client=None
    ):
        """
        Register an agent with the agent manager object.

        :param str name: Name of the agent
        :param str ddo_text: DDO string of the local agent.
        :param DDO ddo: DDO object of the local agent.
        :param str did: Optional did of the agent.
        :param str url: Optional url of the agent, to resolve the ddo and did by calling the agent api.
        :param dict authentication: Authentication dict that can access the agent api
        :param str usrename: Username access for the agent api
        :param str password: Password to access the agent api
        :param str token: Token to access the agent api
        :param object http_client: Test http client to make requests to the agent

        """
        if ddo:
            ddo_text = ddo.as_text

        agent_access = AgentAccess(
            name,
            ddo_text=ddo_text,
            did=did,
            url=url,
            authentication=authentication,
            username=username,
            password=password,
            token=token,
            http_client=http_client
        )
        self._agent_access_items[name] = agent_access

    def unregister_agent(self, name_did_url):
        """

        Removes an agent from the access list of possible cached agents

        :returns: True if found and removed

        """
        for name, agent_access in self._agent_access_items.items():
            if agent_access.is_match(name_did_url):
                del self._agent_access_items[name]
                return True
        return False

    def register_local_agent(self, ddo_text, authentication=None, local_name=None, http_client=None):
        """
        Register a local agent with the  agent manager object.

        :param str ddo_text: DDO string of the local agent.
        :param dict authentication: Authentication dict that can access the local agent
        :param str local_name: Optional local name to use for this agent
        :param object http_client: Test http client to make requests to the agent

        """
        if isinstance(ddo_text, DDO):
            ddo_text = ddo_text.as_text

        if local_name:
            self._local_name = local_name
        agent_access = AgentAccess(self._local_name, ddo_text=ddo_text, authentication=authentication, http_client=http_client)
        self._agent_access_items[self._local_name] = agent_access

    def resolve_agent_url(self, url,  authentication=None, http_client=None):
        """
        Resolve an agent using ony the URL of the remote agent.

        :param str url: URL of the remote agent to resolve
        :param dict authentication: Authentication dict that can access the agent api
        :param object http_client: Test http client to make requests to the agent

        :returns: RemoteAgent object if found, else return None

        """
        ddo = AgentAccess.resolve_agent_url(url, authentication=authentication, http_client=http_client)
        if ddo:
            return RemoteAgent(ddo, authentication=authentication, http_client=http_client)

    def resolve_agent_did(self, did, network=None, authentication=None, http_client=None):
        """
        Resolve an agent using ony the DID of the remote agent. You need to set the network property
        on this object before searching for a did in the network

        :param str did: DID of the remote agent to resolve
        :param Network network: Optional network object to resolve the DID, if not used
            then use the class network value instead

        :param dict authentication: Authentication dict that can access the agent api
        :param object http_client: Test http client to make requests to the agent

        :returns: RemoteAgent object if found, else return None

        """
        if network is None:
            network = self._network
        if not network:
            raise ValueError('No network set to resolve a DID')
        ddo = AgentAccess.resolve_agent_did(did, network)
        if ddo:
            return RemoteAgent(ddo, authentication=authentication, http_client=http_client)

    def load_agent(self, name_did_url, authentication=None):
        """
        Loads and returns a starfish RemoteAgent that is found using the agent name/did/url.

        :param str name_did_url: name, did or url of the agent to find
        :param dict authentication: Optional authentication dict to access this server.

        :returns: RemoteAgent object for the loaded local agent.
        """

        found_agent_access = self.find_agent_access(name_did_url)
        if found_agent_access:
            return found_agent_access.load_agent(authentication=authentication)

    def load_ddo(self, name_did_url, authentication=None):
        """
        Loads and returns a starfish DDO that is found using the agent name/did/url.

        :param str name_did_url: name, did or url of the agent to find
        :param dict authentication: Optional authentication dict to access this server.

        :returns: RemoteAgent object for the loaded local agent.
        """

        found_agent_access = self.find_agent_access(name_did_url)
        if found_agent_access:
            return found_agent_access.ddo

    def find_agent_access(self, name_did_url, auto_resolve=True):
        """

        Finds an agent in the access records of this manager.
        If found return the agent access record

        :param str name_did_url: name/did or url of the agent to find in the access records
        :param bool auto_resolve: If True then if no agent found, try to resolve all of the agents,
            and call again with this field set too False.

        :returns: AgentAccess object if found
        """

        for name, agent_access in self._agent_access_items.items():
            if agent_access.is_match(name_did_url):
                # only return if we have a valid DDO
                if agent_access.ddo:
                    return agent_access

        if auto_resolve:
            self.resolve_access_agents()
            # call again but with no auto_resolve
            return self.find_agent_access(name_did_url, False)

    def is_agent(self, name_did_url):
        """
        Is the name/did or url in the agent access record list

        :param str name_did_url: name/did or url of the agent to find in the access records

        :returns: True if found

        """
        return self.find_agent_access(name_did_url) is not None

    def resolve_access_agents(self):
        """
        Resolve any agents that have only urls. This calls the agent api
        to get the DDO and DID from the agent

        """
        for name, agent_access in self._agent_access_items.items():
            if agent_access.ddo is None:
                if self._network and agent_access.did:
                    agent_access.resolve_did(self._network)
                elif agent_access.url:
                    agent_access.resolve_url()

    def set_http_client(self, value):
        """
        Set all of the agents with the same http_client value.
        This method also clears out any cache with the agent access items

        """

        for name, agent_item in self._agent_access_items.items():
            agent_item.http_client = value
            agent_item.clear_cache()

    def clear_cache(self):
        """
        Clears out the agent items cache.

        """
        for name, agent_item in self._agent_access_items.items():
            agent_item.clear_cache()

    @property
    def local_agent(self):
        """
        Returns the local agent, if it has been registered

        """
        return self.load_agent(self._local_name)

    @property
    def local_agent_name(self):
        return self._local_agent_name

    @property
    def items(self):
        return self._agent_access_items

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, value):
        self._network = value
