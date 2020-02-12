"""
    test_20_invoke_service_free

    As a developer working with Ocean,
    I wish to invoke a free service available on the Ocean ecosystem and obtain the results as a new Ocean Asset

"""

import secrets
import logging
import json
import time
import re

from starfish.asset import OperationAsset
from starfish.job import Job
from starfish.utils.did import did_to_asset_id

INVOKE_TOKENIZE_TEXT_NAME = "Tokenize Text"
INVOKE_INCREMENT_NAME = "Increment"

TEST_TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu congue odio, vel congue sapien. Morbi ac purus ornare, volutpat elit a, lacinia odio. Integer tempor tellus eget iaculis lacinia. Curabitur aliquam, dui vel vestibulum rhoncus, enim metus interdum enim, in sagittis massa est vel velit. Nunc venenatis commodo libero, vitae elementum nulla ultricies id. Aliquam erat volutpat. Cras eu pretium lacus, quis facilisis mauris. Duis sem quam, blandit id tempor in, porttitor at neque. Cras ut blandit risus. Maecenas vitae sodales neque, eu ultricies nibh.'

def _load_operation_asset(remote_agent, invokable_list, name):
    asset_did = invokable_list[name]
    assert(asset_did)
    asset_id = did_to_asset_id(asset_did)
    assert(asset_id)
    asset = remote_agent.get_asset(asset_id)
    assert(asset)
    assert(isinstance(asset, OperationAsset))
    assert(asset.metadata['type'] == 'operation')
    return asset

def assert_tokenize_text(tokens, text):
    values = re.split(r'\W+', text.lower())
    values.pop()
    assert(tokens == values)


def test_20_tokenize_text_sync(remote_agent, invokable_list):

    asset = _load_operation_asset(remote_agent, invokable_list, INVOKE_TOKENIZE_TEXT_NAME)
    inputs = {
        'text': TEST_TEXT
    }
    response = remote_agent.invoke(asset, inputs)
    assert(response)
    assert(response['outputs'])
    assert(response['status'])
    assert(response['status'] == 'succeeded')
    assert_tokenize_text(response['outputs']['tokens'], TEST_TEXT)

def test_20_tokenize_text_async(remote_agent, invokable_list):

    asset = _load_operation_asset(remote_agent, invokable_list, INVOKE_TOKENIZE_TEXT_NAME)

    inputs = {
        'text': TEST_TEXT
    }

    response = remote_agent.invoke(asset, inputs, True)
    assert(response)
    assert(response['job-id'])

    job_id = int(response['job-id'])
    assert(isinstance(job_id, int))

    # wait for job to complete
    time.sleep(1)
    # test get_job
    job = remote_agent.get_job(job_id)
    assert(job)
    assert(isinstance(job, Job))

    # test wait_for_job
    job = remote_agent.job_wait_for_completion(job_id)
    assert(job)
    assert(isinstance(job, Job))
    assert(job.status == 'succeeded')
    assert(job)
    assert_tokenize_text(job.outputs['tokens'], TEST_TEXT)



def test_20_increment_sync(remote_agent, invokable_list):


    value = time.time()
    asset = _load_operation_asset(remote_agent, invokable_list, INVOKE_INCREMENT_NAME)

    inputs = {
        'n': value
    }

    response = remote_agent.invoke(asset, inputs)
    assert(response)
    assert(response['status'])
    assert(response['status'] == 'succeeded')
    assert(response['outputs'])
    assert(float(response['outputs']['n']) - 1 == value)

def test_20_increment_async(remote_agent, invokable_list):

    value = time.time()
    asset = _load_operation_asset(remote_agent, invokable_list, INVOKE_INCREMENT_NAME)


    inputs = {
        'n': value
    }

    response = remote_agent.invoke(asset, inputs, True)
    assert(response)
    assert(response['job-id'])

    job_id = int(response['job-id'])
    assert(isinstance(job_id, int))

    # wait for job to complete
    time.sleep(1)
    # test get_job
    job = remote_agent.get_job(job_id)
    assert(job)
    assert(isinstance(job, Job))

    # test wait_for_job
    job = remote_agent.job_wait_for_completion(job_id)
    assert(job)
    assert(isinstance(job, Job))
    assert(job.status == 'succeeded')
    assert(job)
    assert(float(job.outputs['n']) - 1 == value)

