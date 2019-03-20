

import secrets


class TestConfig():
    keeper_url = 'http://test-keeper-url:1234'
    contracts_path = 'test_artifacts_folder'
    gas_limit = 123456
    accounts = {}
    def __init__(self):
        for index in range(0, 8):
            self.accounts[index] = (secrets.token_hex(32), 'test_password')


testConfig = TestConfig()
