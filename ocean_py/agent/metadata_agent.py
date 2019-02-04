"""
    MetadataAgent - Agent to access the off chain meta storage in squid aka Aquarius
"""

from ocean_py.agent.agent_base import AgentBase
from squid_py.service_agreement.utils import (
    get_sla_template_path,
    register_service_agreement_template
)
from squid_py import (
    ACCESS_SERVICE_TEMPLATE_ID,
    ServiceAgreementTemplate
)

# from ocean_py import logger

class MetadataAgent(AgentBase):
    def __init__(self, ocean):
        """init a standard ocean agent"""
        AgentBase.__init__(self, ocean)

    def register_asset(self, metadata, account):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server
        :param account: account to register the asset
        """
        self.get_registered_access_service_template(account)
        return self._ocean.squid.register_asset(metadata, account)

    def read_asset(self, did):
        """ read the asset metadata(DDO) using the asset DID """
        return self._ocean.squid.resolve_asset_did(did)

    def search_assets(self, text, sort=None, offset=100, page=0):
        ddo_list = self._ocean.squid.search_assets_by_text(text, sort, offset, page)
        return ddo_list

    def get_registered_access_service_template(self, account):
        # register an asset Access service agreement template
        template = ServiceAgreementTemplate.from_json_file(get_sla_template_path())
        template_id = ACCESS_SERVICE_TEMPLATE_ID
        template_owner = self._ocean.squid.keeper.service_agreement.get_template_owner(template_id)
        if not template_owner:
            template = register_service_agreement_template(
                self._ocean.squid.keeper.service_agreement,
                account,
                template,
                self._ocean.squid.keeper.network_name
            )

        return template
