"""

Test provenance


"""
import json
import re
import secrets

from starfish.asset.provenance import Provenance
from starfish.network.did import did_generate_random


def get_activity_id(result):
    assert(result['activity'])
    activity_id = list(result['activity'].keys())[0]
    return activity_id

def assert_prefix(result):
    assert(result['prefix'])
    assert(result['prefix']['xsd'])
    assert(result['prefix']['xsd'] =='http://www.w3.org/2001/XMLSchema#')
    assert(result['prefix']['prov'])
    assert(result['prefix']['prov'] == 'http://www.w3.org/ns/prov#')
    assert(result['prefix']['dep'])
    assert(result['prefix']['dep'] == 'http://datacraft.sg')

def assert_activity(result, activity_id, activity_type, inputs_text=None):
    assert(result['activity'])
    assert(result['activity'][activity_id])
    assert(result['activity'][activity_id]['prov:type']['$'] == f'dep:{activity_type}')
    if inputs_text:
        assert(result['activity'][activity_id]['dep:inputs'])
        assert(result['activity'][activity_id]['dep:inputs']['$'] == inputs_text)


def assert_entity(result, asset_list=None):
    assert(result['entity'])
    assert(result['entity']['dep:this'])
    assert(result['entity']['dep:this']['prov:type'])
    assert(result['entity']['dep:this']['prov:type']['$'] == 'dep:asset')
    if asset_list:
        for asset_did in asset_list:
            assert(result['entity'][asset_did])
            assert(result['entity'][asset_did]['prov:type'])
            assert(result['entity'][asset_did]['prov:type']['$'] == 'dep:asset')
        assert(len(list(result['entity'].keys())) == len(asset_list) + 1)
    else:
        # only one record in the entity the 'dep:this'
        assert(len(list(result['entity'].keys())) == 1)

def assert_was_generated_by(result, activity_id):
    assert(result['wasGeneratedBy'])
    id_dep = list(result['wasGeneratedBy'].keys())[0]
    assert(result['wasGeneratedBy'][id_dep]['prov:entity'] == 'dep:this')
    assert(result['wasGeneratedBy'][id_dep]['prov:activity'] == activity_id)

def assert_agent(result, agent_did):
    assert(result['agent'])
    assert(result['agent'][agent_did])
    assert(result['agent'][agent_did]['prov:type'])
    assert(result['agent'][agent_did]['prov:type']['$'] == 'dep:service-provider')

def assert_was_associated_with(result, activity_id, agent_did):
    assert(result['wasAssociatedWith'])
    id_dep = list(result['wasAssociatedWith'].keys())[0]
    assert(result['wasAssociatedWith'][id_dep]['prov:agent'] == agent_did)
    assert(result['wasAssociatedWith'][id_dep]['prov:activity'] == activity_id)

def assert_was_derived_from(result, asset_list):
    assert(result['wasDerivedFrom'])
    found_list = []
    for random_key, item in result['wasDerivedFrom'].items():
        assert(item['prov:generatedEntity'] == 'dep:this')
        assert(item['prov:usedEntity'] in asset_list)
        found_list.append(item['prov:usedEntity'])

    assert(len(found_list) == len(asset_list))

def test_provenance_create_publish():

    # minimum allowed
    provenance = Provenance()
    result = provenance.create_publish
    assert_prefix(result)
    activity_id = get_activity_id(result)
    assert_activity(result, activity_id, 'publish')
    assert_was_generated_by(result, activity_id)
    assert('agent' not in result)
    assert('wasAssociatedWith' not in result)

    # with agent_did
    agent_did = did_generate_random()
    provenance = Provenance(agent_did)

    result = provenance.create_publish
    assert_prefix(result)
    activity_id = get_activity_id(result)

    assert_activity(result, activity_id, 'publish')
    assert_was_generated_by(result, activity_id)

    assert_agent(result, agent_did)
    assert_was_associated_with(result, activity_id, agent_did)


    # with agent did and activity_id
    agent_did = did_generate_random()
    activity_id = 'abc-123-test'
    provenance = Provenance(agent_did=agent_did, activity_id=activity_id)
    result = provenance.create_publish
    #print(json.dumps(result, indent=4))
    assert_prefix(result)

    assert_activity(result, activity_id, 'publish')
    assert_was_generated_by(result, activity_id)

    assert_agent(result, agent_did)
    assert_was_associated_with(result, activity_id, agent_did)


def test_provenance_create_import():

    # minimum allowed
    provenance = Provenance()

    result = provenance.create_import
    assert_prefix(result)
    activity_id = get_activity_id(result)
    assert_activity(result, activity_id, 'import')
    assert_was_generated_by(result, activity_id)
    assert('agent' not in result)
    assert('wasAssociatedWith' not in result)

    # with agent_did
    agent_did = did_generate_random()

    provenance = Provenance(agent_did=agent_did)
    result = provenance.create_import
    assert_prefix(result)
    activity_id = get_activity_id(result)

    assert_activity(result, activity_id, 'import')
    assert_was_generated_by(result, activity_id)

    assert_agent(result, agent_did)
    assert_was_associated_with(result, activity_id, agent_did)


    # with agent did and activity_id
    agent_did = did_generate_random()
    activity_id = 'abc-123-test'
    provenance = Provenance(agent_did=agent_did, activity_id=activity_id)
    result = provenance.create_import
    assert_prefix(result)

    assert_activity(result, activity_id, 'import')
    assert_was_generated_by(result, activity_id)

    assert_agent(result, agent_did)
    assert_was_associated_with(result, activity_id, agent_did)


def test_provenance_create_invoke():
    # test minimum allowed for create_invoke
    provenance = Provenance()
    result = provenance.create_invoke
    assert_prefix(result)

    activity_id = get_activity_id(result)
    assert_activity(result, activity_id, 'invoke')
    assert_was_generated_by(result, activity_id)
    assert_entity(result)
    assert('agent' not in result)
    assert('wasAssociatedWith' not in result)


    #test all values set for create_invoke
    agent_did = did_generate_random()
    activity_id = 'job-id-123-abc'

    asset_list = []
    for index in range(0, 4):
        asset_id = secrets.token_hex(32)
        asset_list.append(f'{agent_did}/{asset_id}')

    inputs_text = json.dumps(
        {
            'asset_list': 'json'
        }
    )
    provenance = Provenance(agent_did=agent_did, activity_id=activity_id, asset_list=asset_list, inputs_text=inputs_text)
    result = provenance.create_invoke
    assert_prefix(result)

    activity_id = get_activity_id(result)
    assert_activity(result, activity_id, 'invoke', inputs_text)
    assert_was_generated_by(result, activity_id)
    assert_entity(result, asset_list)
    assert_agent(result, agent_did)
    assert_was_associated_with(result, activity_id, agent_did)
    assert_was_derived_from(result, asset_list)
