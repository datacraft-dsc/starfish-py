"""

    Tests for `squid-py issues` for seaching tags in metadata.

"""

import os
import secrets

from web3 import Web3

from tests.integration.squid_issues.example_config import ExampleConfig
from ocean_keeper.account import Account
from squid_py import Ocean
from squid_py import ConfigProvider
from ocean_utils.ddo.ddo import DDO

def test_search_assets():

    # setup test tags to search
    search_tag = secrets.token_hex(32)

    config = ExampleConfig.get_config()
    ConfigProvider.set_config(config)
    ocn = Ocean()

    base_path = os.path.dirname(os.path.realpath(__file__))
    sample_ddo_path = os.path.join(base_path, 'ddo_sa_sample.json')
    assert os.path.exists(sample_ddo_path), "{} does not exist!".format(sample_ddo_path)

    accounts_config = ExampleConfig.get_accounts_config()
    ##########################################################
    # Setup account
    ##########################################################
    publisher = Account(
        Web3.toChecksumAddress(accounts_config['parity.address'].lower()),
        accounts_config['parity.password'],
        accounts_config['parity.keyfile']
    )

    ##########################################################
    # Create an asset DDO with valid metadata
    ##########################################################
    test_ddo = DDO(json_filename=sample_ddo_path)
    test_ddo.metadata['base']['tags']=['test', search_tag]
    test_ddo_dict = test_ddo.as_dictionary()
#    print(test_ddo_dict)
    asset = DDO(dictionary=test_ddo_dict)
    print(asset.metadata['base']['tags'])

    ##########################################################
    # Register using high-level interface
    ##########################################################
    ocn.assets.create(asset.metadata, publisher)

    query = {'query': { 'tags': [search_tag]} }
    ddo_list = ocn.assets.query(query)
    print('ddo list len', len(ddo_list))
    for ddo in ddo_list:
        print('found', ddo.metadata['base']['tags'])
        assert(search_tag in ddo.metadata['base']['tags'])
    assert(len(ddo_list) == 1)
