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
    test_account = convex_accounts[0]
    auto_topup_account(convex_network, test_account)
    test_contract = TestContract(convex_network.convex, test_account)
    contract_address = test_contract.deploy()
    assert(contract_address)
    find_address = test_contract.get_address()
    assert(find_address)
    assert(contract_address == find_address)

    version = test_contract.get_version()
    assert(version)
    assert(version == test_contract.version)
