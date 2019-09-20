#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging
import os

import sys

from squid_py import Config


def get_variable_value(variable):
    if os.getenv(variable) is None:
        logging.error(f'you should provide a {variable}')
        sys.exit(1)
    else:
        return os.getenv(variable)


class ExampleConfig:
    _local_aqua_url = "http://172.15.0.15:5000"
    _local_brizo_url = "http://localhost:8030"
    _duero_aqua_url = "https://aquarius.duero.dev-ocean.com"
    _duero_brizo_url = "https://brizo.duero.dev-ocean.com"
    # _nile_aqua_url = "http://172.15.0.15:5000"

    # _nile_aqua_url = "https://nginx-aquarius.dev-ocean.com"
    # _nile_brizo_url = "https://nginx-brizo.dev-ocean.com"
    # _nile_aqua_url = "https://nginx-aquarius.dev-ocean.com"
    _nile_aqua_url = "https://aquarius.marketplace.dev-ocean.com"
    # _nile_aqua_url = "http://172.15.0.15:5000"
    _nile_brizo_url = "https://brizo.marketplace.dev-ocean.com"
    # _nile_brizo_url = "http://localhost:8030"

    _duero_secret_store_url = "https://secret-store.duero.dev-ocean.com"
    _nile_secret_store_url = "https://secret-store.dev-ocean.com"
    # _nile_secret_store_url = "https://secret-store.marketplace.dev-ocean.com"
    _kovan_keeper_url = "http://localhost:8545"
    _remote_keeper_url = "https://%s.dev-ocean.com"
    _parity_url = "http://localhost:8545"
    _net_to_services_url = {
        'duero': {'aquarius': _duero_aqua_url, 'brizo': _duero_brizo_url},
        'nile': {'aquarius': _nile_aqua_url, 'brizo': _nile_brizo_url},
        'kovan': {'aquarius': _local_aqua_url, 'brizo': _local_brizo_url}
    }
    _net_name_map = {
        'duero': 'duero',
        'duero_local': 'duero',
        'nile': 'nile',
        'nile_local': 'nile',
        'kovan': 'kovan',
        'kovan_local': 'kovan'
    }
    _net_to_env_name = {
        'nile': 'TEST_NILE',
        'nile_local': 'TEST_LOCAL_NILE',
        'duero': 'TEST_DUERO',
        'duero_local': 'TEST_LOCAL_DUERO',
        'spree': 'TEST_LOCAL_SPREE',
        'kovan': 'TEST_KOVAN',
        'kovan_local': 'TEST_LOCAL_KOVAN'
    }

    @staticmethod
    def get_config_net():
        return os.environ.get('TEST_NET', 'spree')

    @staticmethod
    def get_env_name():
        net = ExampleConfig.get_config_net()
        return ExampleConfig._net_to_env_name.get(net)

    @staticmethod
    def get_accounts_config(local_node=True):
        if local_node:
            a, p, k = "0x00bd138abd70e2f00903268f3db08f2d25677c9e", "node0", "tests/resources/account_key_files/key_file_2.json"
            a1, p1, k1 = "0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0", "secret", "tests/resources/account_key_files/key_file_1.json"
        else:
            a, p, k = get_variable_value('PARITY_ADDRESS'), get_variable_value('PARITY_PASSWORD'), get_variable_value('PARITY_KEYFILE')
            a1, p1, k1 = get_variable_value('PARITY_ADDRESS1'), get_variable_value('PARITY_PASSWORD1'), get_variable_value('PARITY_KEYFILE1')

        return {
           "parity.address": a, "parity.password": p, "parity.keyfile": k,
           "parity.address1": a1, "parity.password1": p1, "parity.keyfile1": k1,
        }

    @staticmethod
    def get_base_config(local_node=True):
        config = {
            "keeper-contracts": {
                "keeper.url": "http://localhost:8545",
                "keeper.path": "artifacts",
                "secret_store.url": "http://localhost:12001",
                "parity.url": "http://localhost:8545",
            },
            "resources": {
                "aquarius.url": "http://localhost:5000",
                "brizo.url": "http://localhost:8030",
                "storage.path": "squid_py.db",
                "downloads.path": "consume-downloads"
            }
        }
        config['keeper-contracts'].update(ExampleConfig.get_accounts_config(local_node))
        return config

    @staticmethod
    def _get_config(local_node=True, net_key=''):
        config = ExampleConfig.get_base_config(local_node=local_node)
        net_name = ExampleConfig._net_name_map.get(net_key)
        if net_name == 'kovan':
            config['keeper-contracts']['keeper.url'] = ExampleConfig._kovan_keeper_url
        elif not local_node:
            config['keeper-contracts']['keeper.url'] = ExampleConfig._remote_keeper_url % net_name

        if net_name:
            config['keeper-contracts']['secret_store.url'] = \
                ExampleConfig._duero_secret_store_url if net_name == 'duero' \
                else ExampleConfig._nile_secret_store_url

            service_url = ExampleConfig._net_to_services_url[net_name]
            config['resources']['aquarius.url'] = service_url['aquarius']
            config['resources']['brizo.url'] = service_url['brizo']

        # parity_url maybe different than the keeper_url
        config['keeper-contracts']['parity.url'] = ExampleConfig._parity_url
        return config

    @staticmethod
    def get_config_dict():
        test_net = ExampleConfig.get_config_net()
        local_node = not test_net or test_net in ('nile_local', 'duero_local', 'spree', 'kovan_local')
        config_dict = ExampleConfig._get_config(local_node, test_net)
        return config_dict

    @staticmethod
    def get_config():
        logging.info("Configuration loaded for environment '{}'"
                     .format(ExampleConfig.get_config_net()))
        return Config(options_dict=ExampleConfig.get_config_dict())
