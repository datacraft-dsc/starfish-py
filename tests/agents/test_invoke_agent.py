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

    sch=op.get_schema()
    assert 1==len(sch)
    assert sch[0]=={'name':'firstparam','type':'string'}

    op=agent.get_operation('echo_did')
    assert op
    res=op.invoke(firstparam='ocean')
    assert res['firstparam']=='hello ocean'


