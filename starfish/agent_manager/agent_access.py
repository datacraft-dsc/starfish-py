"""


    AgentAccess


"""
import hashlib
import json
import logging


from starfish.agent import RemoteAgent
from starfish.exceptions import StarfishConnectionError
from starfish.network.ddo import DDO
from starfish.network.did import (
    did_to_id,
    is_did
)

logger = logging.getLogger(__name__)


class AgentAccess:

    def __init__(
        self,
        name,
        ddo_text=None,
        did=None,
        url=None,
        authentication=None,
        username=None,
        password=None,
        token=None,
        http_client=None
    ):
        """
        Create an agent access record. This record tries to obtain all the nesseray information needed to resolve
        an agent.

        :param str name: Name of the agent, this can be used to get the agent information.
        :param str ddo_text: DDO text of the agent if available, if not this class will request for it later.
        :param str did: DID of the agent, similar to ddo_text, the did wil requested later if not available.
        :param str url: URL of the agent.
        :param dict authentication: authentication dict to access the agent
        :param str username: username to access the agent, this can also be in the authentication.
        :param str password: password to access the agent, this can also be in the authentication.
        :param str token: token to access the agent, this can also be in the authentication.

        """
        ddo = None
        if ddo_text:
            ddo = DDO.import_from_text(ddo_text)
            if did is None:
                did = ddo.did

        if authentication is None and (username or token):
            authentication = {}
            if username:
                authentication['username'] = username

            if password:
                authentication['password'] = password

            if token:
                authentication['token'] = token

        self._name = name
        self._url = url
        self._ddo = ddo
        self._did = did
        self._authentication = authentication
        self._agent_cache = {}
        self._http_client = http_client

    @staticmethod
    def resolve_agent_url(url, authentication=None, http_client=None):
        """
        Resolve an agent based on it's url.

        :param str url: URL of the agent
        :param dict authentication: Authentication of the agent.
        :param object http_client: HTTP client to use to access the agent api

        :returns: DDO object of the remote agent
        """
        logger.debug(f'resolving remote agent did from {url}')
        try:
            ddo_text = RemoteAgent.resolve_url(url, authentication=authentication, http_client=http_client)
            if ddo_text:
                return DDO.import_from_text(ddo_text)
        # ignore connetion errors to remote agents
        except StarfishConnectionError:
            pass

    @staticmethod
    def resolve_agent_did(did, network, authentication=None, http_client=None):
        """
        Resolve an agent based on it's DID.

        :param str did: DID of the agent
        :param dict authentication: Authentication of the agent.
        :param object http_client: HTTP client to use to access the agent api

        :returns: DDO object of the remote agent
        """
        return network.resolve_did(did)

    def resolve_url(self):
        """
        Resolve the remote agent using it's URL.

        :param object http_client: HTTP Client to use to access the remote agent api.

        :returns: DDO of the remote agent

        """
        if self._url:
            ddo = AgentAccess.resolve_agent_url(self._url, self._authentication, self._http_client)
            if ddo:
                self._ddo = ddo
                self._did = ddo.did
                return ddo

    def resolve_did(self, network):
        if self._did:
            ddo = AgentAccess.resolve_agent_did(self._did, network)
            if ddo:
                self._ddo = ddo
                self._did = ddo.did
                return ddo

    def is_match(self, name_did_url):
        """
        Is this AgentAccess object matches the name, DID or URL.

        :param str name_did_url: Name, DID or URL to match

        :returns: True if match

        """
        if self._name == name_did_url:
            return True
        if self._url == name_did_url:
            return True
        if self._did and is_did(self._did) and is_did(name_did_url):
            if did_to_id(self._did) == did_to_id(name_did_url):
                return True
        return False

    def load_agent(self, authentication=None, use_cache=True):
        """
        Load this agent and return a starfish RemoteAgent object.

        :param dict authentication: Authentication dict to use to load this agent.
            If None use the authentication in the access object

        :param bool use_cache: If True then use the agent cache to store future requests for remote agents
        :param object http_client: HTTP Client to use to access the agent.

        :returns: Remote Agent object that has been loaded

        """
        agent = None
        if authentication is None:
            authentication = self._authentication
        if use_cache:
            cache_key = self.calc_cache_key(authentication)
            if cache_key not in self._agent_cache:
                # same method but with no cache
                self._agent_cache[cache_key] = self.load_agent(authentication, use_cache=False)
            agent = self._agent_cache[cache_key]
        else:
            if self._ddo is None:
                self.resolve_url(self._http_client)
            logger.debug(f'loading remote agent {self._name}: {self._did}')
            agent = RemoteAgent(self._ddo, authentication=authentication, http_client=self._http_client)

        return agent

    def calc_cache_key(self, authentication=None):
        key_text = [
            self._name
        ]
        if authentication:
            key_text.append(json.dumps(authentication))
        md5hash = hashlib.md5('\n'.join(key_text).encode())
        return md5hash.hexdigest()

    def clear_cache(self):
        """
        Clears out the agent cache

        """
        self._agent_cache = {}

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def ddo(self):
        return self._ddo

    @property
    def did(self):
        return self._did

    @property
    def authentication(self):
        return self._authentication

    @property
    def http_client(self):
        return self._http_client

    @http_client.setter
    def http_client(self, value):
        self._http_client = value

    def __str__(self):
        return f'{self._name} {self._url} {self._did}'
