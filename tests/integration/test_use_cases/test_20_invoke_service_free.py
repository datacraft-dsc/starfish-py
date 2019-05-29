"""
    test_20_invoke_service_free

    As a developer working with Ocean,
    I wish to invoke a free service available on the Ocean ecosystem and obtain the results as a new Ocean Asset

"""

import secrets
import logging
import json

from starfish.asset import OperationAsset
from starfish.job import Job

PRIME_NUMBER_OPERATION_ASSET_ID = "0x8d658b5b09ade5526aecf669e4291c07d88e9791420c09c51d2f922f721858d1"

def test_20_prime_number_sync(surfer_agent):
    
    # this should be get_listing..
    # listing = surfer_agent.get_listing(listing_id)
    
    # at the moment Koi does not create a listing with the asset, so
    # we need to call get_asset instead
    operation_asset = surfer_agent.get_asset(PRIME_NUMBER_OPERATION_ASSET_ID)
    assert(operation_asset)
    print(operation_asset.metadata)
    assert(isinstance(operation_asset, OperationAsset))
    assert(operation_asset.metadata['type'] == 'operation')

    params = {
        'first-n': '11'
    }

    response = surfer_agent.invoke_result(operation_asset, params)
    assert(response)
    print(response)

def test_20_prime_number_async(surfer_agent):
    
    # this should be get_listing..
    # listing = surfer_agent.get_listing(listing_id)
    
    # at the moment Koi does not create a listing with the asset, so
    # we need to call get_asset instead
    operation_asset = surfer_agent.get_asset(PRIME_NUMBER_OPERATION_ASSET_ID)
    assert(operation_asset)
    assert(isinstance(operation_asset, OperationAsset))
    assert(operation_asset.metadata['type'] == 'operation')

    params = {
        'first-n': '11'
    }

    response = surfer_agent.invoke_result(operation_asset, params, True)
    assert(response)
    assert(response['jobid'])

    job_id = response['jobid']
    
    # test get_job
    job = surfer_agent.get_job(job_id)
    assert(job)
    assert(isinstance(job, Job))
    
    # test wait_for_job
    job = surfer_agent.wait_for_job(job_id)
    assert(job)
    assert(isinstance(job, Job))
    print(job)
