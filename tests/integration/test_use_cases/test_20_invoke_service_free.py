"""
    test_20_invoke_service_free

    As a developer working with Ocean,
    I wish to invoke a free service available on the Ocean ecosystem and obtain the results as a new Ocean Asset

"""

import secrets
import logging
import json
import time

from starfish.asset import OperationAsset
from starfish.job import Job

PRIME_NUMBER_OPERATION_ASSET_ID = "0x8d658b5b09ade5526aecf669e4291c07d88e9791420c09c51d2f922f721858d1"
TO_HASH_OPERATION_ASSET_ID = "0x8ade9c7505bcadaab8dacf6848e88ddb4aa6a295612eb01759e35aeb65daeac2"

TEST_HASH_TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu congue odio, vel congue sapien. Morbi ac purus ornare, volutpat elit a, lacinia odio. Integer tempor tellus eget iaculis lacinia. Curabitur aliquam, dui vel vestibulum rhoncus, enim metus interdum enim, in sagittis massa est vel velit. Nunc venenatis commodo libero, vitae elementum nulla ultricies id. Aliquam erat volutpat. Cras eu pretium lacus, quis facilisis mauris. Duis sem quam, blandit id tempor in, porttitor at neque. Cras ut blandit risus. Maecenas vitae sodales neque, eu ultricies nibh.'

def test_20_prime_number_sync(surfer_agent):

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

    response = surfer_agent.invoke_result(operation_asset, params)
    assert(response)
    assert(response['results'])
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

    job_id = int(response['jobid'])
    assert(isinstance(job_id, int))

    # FIXME: bug in koi, can return an empty job status record, straight after job creation
    time.sleep(1)
    # test get_job
    job = surfer_agent.get_job(job_id)
    assert(job)
    assert(isinstance(job, Job))

    # test wait_for_job
    job = surfer_agent.job_wait_for_completion(job_id)
    assert(job)
    assert(isinstance(job, Job))
    assert(job.status == 'succeeded' or job.status == 'completed')
    assert(job.results)
    print(job)



def test_20_to_hash_sync(surfer_agent):

    # this should be get_listing..
    # listing = surfer_agent.get_listing(listing_id)

    # at the moment Koi does not create a listing with the asset, so
    # we need to call get_asset instead
    operation_asset = surfer_agent.get_asset(TO_HASH_OPERATION_ASSET_ID)
    assert(operation_asset)
    assert(isinstance(operation_asset, OperationAsset))
    assert(operation_asset.metadata['type'] == 'operation')

    params = {
        'to-hash': TEST_HASH_TEXT
    }

    response = surfer_agent.invoke_result(operation_asset, params)
    assert(response)
    assert(response['results'])
    print(response)

def test_20_to_hash_async(surfer_agent):

    # this should be get_listing..
    # listing = surfer_agent.get_listing(listing_id)

    # at the moment Koi does not create a listing with the asset, so
    # we need to call get_asset instead
    operation_asset = surfer_agent.get_asset(TO_HASH_OPERATION_ASSET_ID)
    assert(operation_asset)
    assert(isinstance(operation_asset, OperationAsset))
    assert(operation_asset.metadata['type'] == 'operation')

    params = {
        'to-hash': TEST_HASH_TEXT
    }

    response = surfer_agent.invoke_result(operation_asset, params, True)
    assert(response)
    assert(response['jobid'])

    job_id = int(response['jobid'])
    assert(isinstance(job_id, int))

    # FIXME: bug in koi, can return an empty job status record, straight after job creation
    time.sleep(1)

    # test get_job
    job = surfer_agent.get_job(job_id)
    assert(job)
    assert(isinstance(job, Job))


    # test wait_for_job
    job = surfer_agent.job_wait_for_completion(job_id)
    assert(job)
    assert(isinstance(job, Job))
    assert(job.status == 'completed')
    assert(job.results)
    print(job)
