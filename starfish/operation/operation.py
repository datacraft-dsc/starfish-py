
"""
    Operation class
"""

import logging
from starfish.account import Account
from starfish.operation.aoperation import AOperation
logger = logging.getLogger('ocean')
import requests
import json

class Operation(AOperation):
    """

    This class returns an operation that can be invoked on a remote Ocean Invoke server 
    :param agent: agent that was used create this object.
    :type agent: :class:`.Agent`
    :param did: the did of this Operation
    :type did: str

    """

    def __init__(self, agent,did):
        """init the the Operation Object Base with the agent instance"""
        super().__init__(agent, did)
        self.agent=agent
        self.did=did
        r=requests.get(agent._koi_url+'operation/'+did)
        self.schema=json.loads(r.text)
        self.argnames=[i['name'] for i in self.schema]

    def get_schema(self):
        """
        returns the schema for this particular operation
        """
        return self.schema

    def invoke(self, **kwargs):
        """
        Call the invoke function with keyword arguments. The keywords should be argument names required in the invoke function payload.
        returns the payload returned by the operation, or ValueError.
        """
        logger.info(f'calling invoke in operation.py with payload: {kwargs}')
        #test if the keyword arguments are valid
        valid_args=len(frozenset(self.argnames).intersection(kwargs.keys()))==len(kwargs)
        if True==valid_args:
            r=requests.post(self.agent._koi_url+'freeinvoke/'+self.did,json=kwargs)
            j=json.loads(r.text)
            return j
        else:
            raise ValueError("Invalid arguments ") 

