"""
    Test invoke agent

"""

import pathlib
import json
import logging
import time

from starfish import (
    Ocean,
    logger
)
from starfish.agent.invoke_agent import InvokeAgent

logger = logging.getLogger('test.invoke')

# koi is not working with the current version of keeper 0.9.0

def _test_invoke():

    agent = InvokeAgent()
    assert agent

    result = agent.get_operations()
    assert 'hashing_did' == result['hashing']
    assert 'echo_did' == result['echo']

    operation = agent.get_operation('echo_did')
    assert operation

    schema = operation.get_schema()
    assert 1 == len(schema)
    assert schema['firstparam'] == 'string'

    result = operation.invoke(firstparam='ocean')
    assert result['firstparam'] == 'hello ocean'


