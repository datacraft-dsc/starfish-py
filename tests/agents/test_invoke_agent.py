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

from starfish.logging import setup_logging

setup_logging(level=logging.DEBUG)


def test_invoke():

    agent = InvokeAgent()
    assert agent

    res=agent.get_operations()
    assert 'hashing_did'==res['hashing']
    assert 'echo_did'==res['echo']

    op=agent.get_operation('echo_did')
    assert op

    sch=op.get_schema()
    assert 1==len(sch)
    assert sch['firstparam']=='string'

    res=op.invoke(firstparam='ocean')
    assert res['firstparam']=='hello ocean'


