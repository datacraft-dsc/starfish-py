
"""
    Operation class
"""

import logging
from starfish.operation.operation_base import OperationBase
from collections import ChainMap
import requests
import json

logger = logging.getLogger('starfish.operiation')

class Operation(OperationBase):
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

    def get_schema(self):
        """
        returns the schema for this particular operation
        """
        r=requests.get(self.agent._koi_url+'operation/'+self.did)
        rawjson=json.loads(r.text)
        self.argnames=[i['name'] for i in rawjson]
        logger.info(f' rawjson {rawjson}')
        self.schema=dict(zip(self.argnames,[i['type'] for i in rawjson]))
        return self.schema

    def _payload(self,account,k,v):
        if self.schema.get(k)=='asset':
            if isinstance(v,Asset):
                return {k:{'service_agreement_id':v.purchase_id, 'account':account}}
            raise ValueError("Invalid arguments ")
        else:
            return {k:v}

    def invoke(self, **kwargs):
        """
        Call the invoke function with keyword arguments.
        The keywords should be argument names required in the invoke function payload.
        returns the payload returned by the operation, or ValueError.
        This parameterization of invoke takes only string arguments (and not Ocean assets).
        """
        ## check if all the args are present
        valid_args=len(frozenset(self.argnames).intersection(kwargs.keys()))==len(kwargs)
        ## check if args are not of 'asset' type
        string_args_only=len([k for k,v in kwargs.items() if self.schema.get(k)=='string'])==len(kwargs)
        logger.info(f' valid args {valid_args} string args {string_args_only}')
        #if True==valid_args and string_args_only==True:
        if True==valid_args:
            r=requests.post(self.agent._koi_url+'freeinvoke/'+self.did,json=kwargs)
            j=json.loads(r.text)
            return j
        else:
            raise ValueError("Invalid arguments ")

    def invoke_op(self,account, **kwargs):
        """
        Call the invoke function with keyword arguments which could have Ocean params (hence invoke_op) The keywords should be argument names required in the invoke function payload.
        returns the payload returned by the operation, or ValueError.
        """
        logger.info(f'calling invoke in operation.py with payload: {kwargs}')
        #test if the keyword arguments are valid
        valid_args=len(frozenset(self.argnames).intersection(kwargs.keys()))==len(kwargs)
        if True==valid_args:
            try:
                payload_seq=[_payload(account,k,v) for k,v in kwargs.items()]
                payload=dict(ChainMap(*payload_seq))

                r=requests.post(self.agent._koi_url+'freeinvoke/'+self.did,json=payload)
                j=json.loads(r.text)
                return j
            except ValueError:
                raise ValueError(" arguments are invalid according to the schema defn " )
        else:
            raise ValueError("Invalid arguments ")
