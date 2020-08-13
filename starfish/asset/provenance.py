"""

    Provenance module

"""
import secrets
from typing import Any

PROVENANCE_DEP = 'dep'
PROVENANCE_ACTIVITY_TYPE_PUBLISH = 'publish'
PROVENANCE_ACTIVITY_TYPE_IMPORT = 'import'
PROVENANCE_ACTIVITY_TYPE_INVOKE = 'invoke'

PROVENANCE_AGENT_TYPE_SERVICE_PROVIDER = 'service-provider'
PROVENANCE_ACTIVITY_ID_LENGTH = 32
PROVENANCE_REFERENCE_ID_LENGTH = 32


def create_publish(agent_did: str = None, activity_id: str = None) -> Any:
    """

    Return a publish provenance metadata dict. This is called before an asset is published to an agent.

    :param str agent_did: DID of the agent this asset is going to be published too.
    :param str activity_id: Activity id that can be set with this provenance, if not set ,then a random
        value will be set
    """
    return generate_publish_import(PROVENANCE_ACTIVITY_TYPE_PUBLISH, agent_did, activity_id)


def create_import(agent_did: str = None, activity_id: str = None) -> Any:
    """

    Return an import provenance records as a dict. This is called before a copied asset is published to an agent.

    :param str agent_did: Optional did of the agent that this asset is being published too.
    :param str activity_id: Activity id that can be set with this provenance, if not set ,then a random
        value will be set
    """
    return generate_publish_import(PROVENANCE_ACTIVITY_TYPE_IMPORT, agent_did, activity_id)


def create_invoke(
    agent_did: str = None,
    activity_id: str = None,
    asset_list: Any = None,
    inputs_text: str = None,
    outputs_text: str = None
) -> Any:

    if activity_id is None:
        activity_id = generate_activity_id()

    entities = generate_asset_entity()
    if asset_list:
        for asset_did in asset_list:
            entities = generate_asset_entity(asset_did, entities)

    dependencies = None
    if inputs_text or outputs_text:
        dependencies = generate_dependencies(inputs_text, outputs_text)

    result = {
        'prefix': generate_prefix(),
        'activity': generate_activity(activity_id, PROVENANCE_ACTIVITY_TYPE_INVOKE, dependencies),
        'entity': entities,
        'wasGeneratedBy': generate_was_generated_by(activity_id)
    }
    if agent_did:
        result['agent'] = generate_agent(agent_did, PROVENANCE_AGENT_TYPE_SERVICE_PROVIDER)
        result['wasAssociatedWith'] = generate_was_associated_with(agent_did, activity_id)

    if asset_list:
        result['wasDerivedFrom'] = generate_was_derived_from(asset_list)
    return result


def generate_publish_import(activity_type: str, agent_did: str = None, activity_id: str = None) -> Any:
    """

    Return a publish provenance metadata dict. This is called before an asset is published to an agent.

    :param str agent_did: Optional Agent DID of the agent this asset is going to be published too.
    :param str activity_id: Activity id that can be set with this provenance, if not set ,then a random
        value will be set
    """
    if activity_id is None:
        activity_id = generate_activity_id()

    result = {
        'prefix': generate_prefix(),
        'activity': generate_activity(activity_id, activity_type),
        'entity': generate_asset_entity(),
        'wasGeneratedBy': generate_was_generated_by(activity_id)
    }

    if agent_did:
        result['agent'] = generate_agent(agent_did, PROVENANCE_AGENT_TYPE_SERVICE_PROVIDER)
        result['wasAssociatedWith'] = generate_was_associated_with(agent_did, activity_id)

    return result


def generate_prefix() -> Any:
    return {
        'xsd': 'http://www.w3.org/2001/XMLSchema#',
        'prov': 'http://www.w3.org/ns/prov#',
        PROVENANCE_DEP: 'http://dex.sg'
    }


def generate_asset_entity(asset_did: str = None, entities: Any = None) -> Any:
    if entities is None:
        entities = {}
    if asset_did is None:
        asset_did = f'{PROVENANCE_DEP}:this'
    entities[asset_did] = {
        'prov:type': {
            '$': f'{PROVENANCE_DEP}:asset',
            'type': 'xsd:string'
        }
    }
    return entities


def generate_activity(activity_id: str, activity_type: str, entries: Any = None) -> Any:
    items = {
        'prov:type': {
            '$': f'{PROVENANCE_DEP}:{activity_type}',
            'type': 'xsd:string'
        }
    }
    if entries:
        for name, value in entries.items():
            items[name] = value

    return {
        f'{PROVENANCE_DEP}:{activity_id}': items
    }


def generate_agent(agent_did: str, agent_type: str) -> Any:
    return {
        f'{agent_did}': {
            'prov:type': {
                '$': f'{PROVENANCE_DEP}:{agent_type}',
                'type': 'xsd:string'
            }
        }
    }


def generate_was_associated_with(agent_did: str, activity_id: str) -> Any:
    random_id = generate_random_id()
    return {
        f'_:{random_id}': {
            'prov:agent': agent_did,
            'prov:activity': activity_id
        }
    }


def generate_was_generated_by(activity_id: str) -> Any:
    entity_id = f'{PROVENANCE_DEP}:this'
    random_id = generate_random_id()
    return {
        f'_:{random_id}': {
            'prov:entity': entity_id,
            'prov:activity': activity_id
        }
    }


def generate_was_derived_from(asset_list: Any) -> Any:
    entities = {}
    for asset_did in asset_list:
        random_id = generate_random_id()
        entities[f'_:{random_id}'] = {
            'prov:usedEntity': asset_did,
            'prov:generatedEntity': f'{PROVENANCE_DEP}:this'
        }
    return entities


def generate_dependencies(inputs_text: str, outputs_text: str) -> Any:
    result = {}
    if inputs_text:
        result[f'{PROVENANCE_DEP}:inputs'] = {
            '$': inputs_text,
            'type': 'xsd:string'
        }
    if outputs_text:
        result[f'{PROVENANCE_DEP}:outputs'] = {
            '$': outputs_text,
            'type': 'xsd:string'
        }
    return result


def generate_activity_id() -> str:
    return secrets.token_hex(PROVENANCE_ACTIVITY_ID_LENGTH)


def generate_random_id() -> str:
    random_id = secrets.token_hex(PROVENANCE_REFERENCE_ID_LENGTH)
    return random_id
