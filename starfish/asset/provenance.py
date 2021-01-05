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


class Provenance:
    def __init__(self, agent_did: str = None, activity_id: str = None, asset_list: Any = None, inputs_text: str = None):
        """
        :param str agent_did: Agent DID that the invoke was executed on
        :param str activity_id: Activity id or invoke job id that was used to run the invoke, or job to create the asset
        :param list[str] asset_list: List of asset DID's that was used to call the invoke operation
        :param str inputs_text: the JSON string of the input fields

        """

        self._agent_did = agent_did
        self._activity_id = activity_id
        self._asset_list = asset_list
        self._inputs_text = inputs_text
        if self._activity_id is None:
            self._activity_id = self._generate_activity_id()

        self._index_items = {
            'wasAssociatedWith': {
                'prefix': 'assoc_',
                'index': 1,
            },
            'wasGeneratedBy': {
                'prefix': 'gen_',
                'index': 1,
            },
            'wasDerivedFrom': {
                'prefix': 'derived_',
                'index': 1,
            },
        }

    @property
    def create_publish(self) -> Any:
        """

        Return a publish provenance metadata dict. This is called before an asset is published to an agent.

        :param str agent_did: DID of the agent this asset is going to be published too.
        :param str activity_id: Activity id that can be set with this provenance, if not set ,then a random
            value will be set
        """
        return self._generate_publish_import(PROVENANCE_ACTIVITY_TYPE_PUBLISH)

    @property
    def create_import(self) -> Any:
        """

        Return an import provenance records as a dict. This is called before a copied asset is published to an agent.

        :param str agent_did: Optional did of the agent that this asset is being published too.
        :param str activity_id: Activity id that can be set with this provenance, if not set ,then a random
            value will be set
        """
        return self._generate_publish_import(PROVENANCE_ACTIVITY_TYPE_IMPORT)

    @property
    def create_invoke(self) -> Any:

        """

        Create a provenance invoke dict.

        :returns: a dict of the provenance metadata
        """

        entities = self._generate_asset_entity()
        if self._asset_list:
            for asset_did in self._asset_list:
                entities = self._generate_asset_entity(asset_did, entities)

        dependencies = None
        if self._inputs_text:
            dependencies = self._generate_dependencies(self._inputs_text)

        result = {
            'prefix': self._generate_prefix,
            'activity': self._generate_activity(self._activity_id, PROVENANCE_ACTIVITY_TYPE_INVOKE, dependencies),
            'entity': entities,
            'wasGeneratedBy': self._generate_was_generated_by(self._activity_id)
        }
        if self._agent_did:
            result['agent'] = self._generate_agent(self._agent_did, PROVENANCE_AGENT_TYPE_SERVICE_PROVIDER)
            result['wasAssociatedWith'] = self._generate_was_associated_with(self._agent_did, self._activity_id)

        if self._asset_list:
            result['wasDerivedFrom'] = self._generate_was_derived_from(self._asset_list)
        return result

    def _generate_publish_import(self, activity_type: str) -> Any:
        """

        generate a import or publish provenance metadata dict. This is called before an asset is published to an agent.

        :param str agent_did: Optional Agent DID of the agent this asset is going to be published too.
        :param str activity_id: Activity id that can be set with this provenance, if not set ,then a random
            value will be set
        """

        result = {
            'prefix': self._generate_prefix,
            'activity': self._generate_activity(self._activity_id, activity_type),
            'entity': self._generate_asset_entity(),
            'wasGeneratedBy': self._generate_was_generated_by(self._activity_id)
        }

        if self._agent_did:
            result['agent'] = self._generate_agent(self._agent_did, PROVENANCE_AGENT_TYPE_SERVICE_PROVIDER)
            result['wasAssociatedWith'] = self._generate_was_associated_with(self._agent_did, self._activity_id)

        return result

    @property
    def _generate_prefix(self) -> Any:
        return {
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'prov': 'http://www.w3.org/ns/prov#',
            PROVENANCE_DEP: 'http://datacraft.sg'
        }

    def _generate_asset_entity(self, asset_did: str = None, entities: Any = None) -> Any:
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

    def _generate_activity(self, activity_id: str, activity_type: str, entries: Any = None) -> Any:
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
            f'{activity_id}': items
        }

    def _generate_agent(self, agent_did: str, agent_type: str) -> Any:
        return {
            f'{agent_did}': {
                'prov:type': {
                    '$': f'{PROVENANCE_DEP}:{agent_type}',
                    'type': 'xsd:string'
                }
            }
        }

    def _generate_was_associated_with(self, agent_did: str, activity_id: str) -> Any:
        new_id = self._generate_unique_id('wasAssociatedWith')
        return {
            f'_:{new_id}': {
                'prov:agent': agent_did,
                'prov:activity': activity_id
            }
        }

    def _generate_was_generated_by(self, activity_id: str) -> Any:
        entity_id = f'{PROVENANCE_DEP}:this'
        new_id = self._generate_unique_id('wasGeneratedBy')
        return {
            f'_:{new_id}': {
                'prov:entity': entity_id,
                'prov:activity': activity_id
            }
        }

    def _generate_was_derived_from(self, asset_list: Any) -> Any:
        entities = {}
        for asset_did in asset_list:
            new_id = self._generate_unique_id('wasDerivedFrom')
            entities[f'_:{new_id}'] = {
                'prov:usedEntity': asset_did,
                'prov:generatedEntity': f'{PROVENANCE_DEP}:this'
            }
        return entities

    def _generate_dependencies(self, inputs_text: str) -> Any:
        result = {}
        if inputs_text:
            result[f'{PROVENANCE_DEP}:inputs'] = {
                '$': inputs_text,
                'type': 'xsd:string'
            }
        return result

    def _generate_activity_id(self) -> str:
        return secrets.token_hex(PROVENANCE_ACTIVITY_ID_LENGTH)

    def _generate_unique_id(self, name) -> str:
        item = self._index_items[name]
        new_id = f"{item['prefix']}{item['index']}"
        item['index'] += 1
        return new_id
