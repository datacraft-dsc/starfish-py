"""

    Provenance class to create provenance metadata


"""

import secrets

PROVENANCE_DEP = 'dep'
PROVENANCE_ACTIVITY_TYPE_PUBLISH = 'publish'
PROVENANCE_ACTIVITY_TYPE_PUBLISH = 'import'
PROVENANCE_ACTIVITY_TYPE_OPERATION = 'operation'

PROVENANCE_AGENT_TYPE_ACCOUNT = 'account'


def create_publish(agent_id, activity_id=None):
    if activity_id is None:
        activity_id = secrets.token_hex(32)

    return {
        'prefix': create_prefix(),
        'activity': create_activity(activity_id, PROVENANCE_ACTIVITY_TYPE_PUBLISH),
        'entity': create_asset_entity('this'),
        'agent': create_agent(agent_id, PROVENANCE_AGENT_TYPE_ACCOUNT),
        'wasAssociatedWith': create_associated_with(agent_id, activity_id),
        'wasGeneratedBy': create_generated_by(activity_id)
    }


def create_prefix():
    return {
        'xsd': 'http://www.w3.org/2001/XMLSchema#',
        'prov': 'http://www.w3.org/ns/prov#',
        PROVENANCE_DEP: 'http://dex.sg'
    }


def create_asset_entity(asset_id):
    return {
        f'{PROVENANCE_DEP}:{asset_id}': {
            'prov:type': {
                '$': f'{PROVENANCE_DEP}:asset',
                'type': 'xsd:string'
            }
        }
    }


def create_activity(activity_id, activity_type):
    return {
        f'{PROVENANCE_DEP}:{activity_id}': {
            'prov:type': {
                '$': f'{PROVENANCE_DEP}:{activity_type}',
                'type': 'xsd:string'
            }
        }
    }


def create_agent(agent_id, agent_type):
    return {
        f'{PROVENANCE_DEP}:{agent_id}': {
            'prov:type': {
                '$': f'{PROVENANCE_DEP}:{agent_type}',
                'type': 'xsd:string'
            }
        }
    }


def create_associated_with(agent_id, activity_id):
    random_id = secrets.token_hex(32)
    return {
        f'_:{random_id}': {
            'prov:agent': agent_id,
            'prov:activity': activity_id
        }
    }


def create_generated_by(activity_id):
    entity_id = f'{PROVENANCE_DEP}:this'
    random_id = secrets.token_hex(32)
    return {
        f'_:{random_id}': {
            'prov:entity': entity_id,
            'prov:activity': activity_id
        }
    }
