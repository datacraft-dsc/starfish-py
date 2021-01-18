"""

    Agent Manager


"""

from starfish.agent import RemoteAgent
from starfish.agent_manager.agent_access import AgentAccess
from starfish.network.ddo import DDO

LOCAL_AGENT_NAME = '_local_agent'


class AgentManager:

    def __init__(self, http_client=None):
        """
        Create an agent manager object to resolve agents and keep a list of knwon agents.
        If the list of known agents only have a url, then the agent manager will try
        to resolve the url's to DID's, using the api call to obtain the DDO from the
        remote agents.

        """
        self._agent_access_list = []
        self._local_name = LOCAL_AGENT_NAME
        self._http_client = http_client

    def register_agents(self, agents):
        """
        Register a dict of agents and their url/did and access information.
        This allows the agent manager to resolve 'agent names'.
        So that you can pass a given name for the agent

        :param dict agents: Dict of agents that can be stored in the agent manager.

        """
        if not isinstance(agents, dict):
            raise TypeError('agents parameter must be a type dict')

        for name, agent in agents.items():
            agent_access = AgentAccess(
                name,
                url=agent.get('url', None),
                did=agent.get('did', None),
                username=agent.get('username', None),
                password=agent.get('password', None),
                token=agent.get('token', None),
            )
            self._agent_access_list.append(agent_access)

    def register_local_agent(self, ddo_text, authentication=None, local_name=None):
        """
        Register a local agent with the  agent manager object.

        :param str ddo_text: DDO string of the local agent.
        :param dict authentication: Authentication dict that can access the local agent
        :param str local_name: Optional local name to use for this agent

        """
        if isinstance(ddo_text, DDO):
            ddo_text = ddo_text.as_text

        self._agent_access_list = []
        if local_name:
            self._local_name = local_name
        agent_access = AgentAccess(self._local_name, ddo_text=ddo_text, authentication=authentication)
        self._agent_access_list.append(agent_access)

    def resolve_agent_url(self, url,  authentication=None):
        """
        Resolve an agent using ony the URL of the remote agent.

        :param str url: URL of the remote agent to resolve

        :returns: RemoteAgent object if found, else return None

        """
        ddo = AgentAccess.resolve_agent_url(url, authentication=authentication, http_client=self._http_client)
        if ddo:
            return RemoteAgent(ddo, authentication=authentication, http_client=self._http_client)

    def resolve_agent_did(self, did,  authentication=None):
        """
        Resolve an agent using ony the DID of the remote agent.

        :param str did: DID of the remote agent to resolve

        :returns: RemoteAgent object if found, else return None

        """
        ddo = AgentAccess.resolve_agent_url(did, authentication=authentication, http_client=self._http_client)
        if ddo:
            return RemoteAgent(ddo, authentication=authentication, http_client=self._http_client)

    def load_agent(self, name_did_url, authentication=None):
        """
        Loads and returns a starfish RemoteAgent that is found using the agent name/did/url.

        :param str name_did_url: name, did or url of the agent to find
        :param dict authentication: Optional authentication dict to access this server.

        :returns: RemoteAgent object for the loaded local agent.
        """

        found_agent_access = self.find_agent_access(name_did_url)
        if found_agent_access:
            return found_agent_access.load_agent(authentication=authentication, http_client=self._http_client)

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

        for agent_access in self._agent_access_list:
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
        for agent_access in self._agent_access_list:
            if agent_access.did is None and agent_access.url:
                agent_access.resolve_url(http_client=self._http_client)

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
    def access_items(self):
        return self._agent_access_list

    @property
    def http_client(self):
        return self._http_client

    @http_client.setter
    def http_client(self, value):
        self._http_client = value
        found_agent_access = self.find_agent_access(self._local_name)
        if found_agent_access:
            found_agent_access.clear_cache()
