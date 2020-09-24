"""

    Test ContractBase

"""

import pytest
import secrets
from tests.integration.network.convex.helpers import auto_topup_account

from starfish.network.convex.contract.contract_base import ContractBase


class TestContract(ContractBase):
    def __init__(self, convex, account):
        ContractBase.__init__(self, convex, account, 'storage-example', '0.0.1')
        self._source = f'''

    (def stored-data nil )
    (defn version [] "{self.version}")
    (defn get [] stored-data)
    (defn set [x] (def stored-data x))
    (export get set version)
'''


def test_contract_base_deploy(convex_network, convex_accounts):
    auto_topup_account(convex_network, convex_accounts)

    test_account = convex_accounts[0]
    other_account = convex_accounts[1]

    test_contract = TestContract(convex_network.convex, test_account)
    contract_address = test_contract.deploy()
    assert(contract_address)
    find_address = test_contract.get_address()
    assert(find_address)
    assert(contract_address == find_address)

    version = test_contract.get_version()
    assert(version)
    assert(version == test_contract.version)

    # test load
    test_contract_instance = TestContract(convex_network.convex, test_account)
    test_contract_instance.load()
    assert(test_contract_instance.address == test_contract.address)
    assert(test_contract_instance.version == test_contract.version)


    # test load using a different account
    test_contract_instance = TestContract(convex_network.convex, test_account.address)
    test_contract_instance.load()
    assert(test_contract_instance.address == test_contract.address)
    assert(test_contract_instance.version == test_contract.version)

    with pytest.raises(TypeError, match='with a valid convex account'):
        test_contract_instance.deploy()
