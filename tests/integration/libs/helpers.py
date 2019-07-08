
"""

Squid Helpers

"""
from squid_py.brizo.brizo_provider import BrizoProvider
from tests.integration.mocks.brizo_mock import BrizoMock


"""
def setup_squid_purchase(ocean, listing, account):
    BrizoProvider.set_brizo_class(BrizoMock)
    mock = BrizoProvider.get_brizo()

    model = ocean.get_squid_model()
    ddo = model._squid_ocean.assets.resolve(listing.asset.did)
    mock.subscribe(ocean, account._squid_account, listing.asset.did, ddo)
"""
