"""

    Tests for `squid-py issues`.

"""


from tests.integration.squid_issues.example_config import ExampleConfig
from squid_py import Ocean
from squid_py import ConfigProvider

def search_assets():
    config = ExampleConfig.get_config()
    ConfigProvider.set_config(config)
    ocn = Ocean()

    sample_ddo_path = get_resource_path('ddo', 'ddo_sa_sample.json')
    assert sample_ddo_path.exists(), "{} does not exist!".format(sample_ddo_path)

    ##########################################################
    # Setup account
    ##########################################################
    publisher = ocn.main_account

    # You will need some token to make this transfer!
    assert publisher_ocean_instance.accounts.balance(publisher).ocn > 0

    ##########################################################
    # Create an asset DDO with valid metadata
    ##########################################################
    asset = DDO(json_filename=sample_ddo_path)

    ##########################################################
    # Register using high-level interface
    ##########################################################
    ocn.assets.create(asset.metadata, publisher)
