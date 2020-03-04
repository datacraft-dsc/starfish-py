"""


    Contract Manager

    loads contracts


"""

import importlib
import inspect
import logging
import json
import os

from .contract_base import ContractBase

from web3 import Web3, HTTPProvider

DEFAULT_PACKAGE_NAME = 'starfish.contract'

NETWORK_NAMES = {
    0: 'development',
    1: 'main',
    2: 'morden',
    3: 'ropsten',
    4: 'rinkeby',
    42: 'kovan',
    8995: 'nile',           # Ocean Protocol Public test net
    8996: 'spree'           # Ocean Protocol local test net
}


logger = logging.getLogger(__name__)


class ContractManager:

    def __init__(self, network_url):
        self._network_url = network_url
        self._web3 = None
        self.connect()

    def connect(self):
        self._web3 = Web3(HTTPProvider(self._network_url))
        if self._web3:
            self._network_name = ContractManager.find_network_name_from_id(int(self._web3.version.network))
            logger.info(f'connected to {self._network_name}')

    def load(self, name, package_name=None):
        if package_name is None:
            package_name = DEFAULT_PACKAGE_NAME
        package_module = importlib.import_module(package_name)
        for item in inspect.getmembers(package_module, inspect.ismodule):
            if item[0] == name:
                class_list = ContractManager._find_class_list_in_module(item[1])
                return self.create_contract(name, class_list[0])
        return None


    def create_contract(self, name, class_def):
        contract_object = class_def()
        contract_name = contract_object.name
        print(contract_name)
        abi_filename = ContractManager.find_abi_filename(contract_name, self.network_name)
        if abi_filename:
            contract_info = ContractManager.load_abi_file(abi_filename)
            contract_object.load(self.web3, abi=contract_info['abi'], address=contract_info['address'])
        print(abi_filename)
        return contract_object

    @property
    def network_url(self):
        return self._network_url

    @property
    def network_name(self):
        return self._network_name

    @property
    def web3(self):
        return self._web3

    @staticmethod
    def _find_class_list_in_module(contract_module):
        class_list = []
        for name, obj in inspect.getmembers(contract_module, inspect.isclass):
            if issubclass(obj, ContractBase) and (name != 'ContractBase'):
                class_list.append(obj)
        return class_list

    @staticmethod
    def find_network_name_from_id(network_id):
        if network_id in NETWORK_NAMES:
            return NETWORK_NAMES[network_id]
        return NETWORK_NAMES[0]

    @staticmethod
    def find_abi_filename(name, network_name):
        filename = f'{name}.{network_name}.json'
        test_file = os.path.join('artifacts', filename)
        if os.path.exists(test_file):
            return test_file
        return None

    @staticmethod
    def load_abi_file(filename):
        if filename and os.path.exists(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)