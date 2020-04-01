"""


    Contract Manager

    loads contracts


"""

import gzip
import importlib
import inspect
import json
import logging
import os

from starfish.contract.contract_base import ContractBase

logger = logging.getLogger(__name__)


ARTIFACT_DATA_FILENAME = 'artifacts.json.gz'


class ContractManager:

    def __init__(self, web3, default_package_name):
        self._web3 = web3
        self._default_package_name = default_package_name
        self._artifact_items = ContractManager.load_artifact_library(ARTIFACT_DATA_FILENAME)

    def load(self, name, network_name, abi_filename=None, package_name=None):
        if package_name is None:
            package_name = self._default_package_name
        if package_name is None:
            raise ValueError(f'You need to provide a package name for the contract classes')

        package_module = importlib.import_module(package_name)
        for item in inspect.getmembers(package_module, inspect.ismodule):
            class_def = ContractManager._find_class_in_module(name, item[1])
            if class_def:
                return self.create_contract(name, network_name, class_def, abi_filename)
        return None

    def create_contract(self, name, network_name, class_def, abi_filename=None):
        contract_object = class_def()
        contract_name = contract_object.name

        # abi_filename can be False, so that we do not need to load a contract info
        if abi_filename is None or abi_filename:
            contract_info = self.get_contract_data(network_name, contract_name, abi_filename)
            if contract_info:
                contract_object.load(self.web3, abi=contract_info['abi'], address=contract_info['address'])
            else:
                raise FileNotFoundError(f'Cannot find artifact data for contract {contract_name}.{network_name}')
        else:
            # load in an dummy contract with no abi or address
            contract_object.load(self.web3)

        return contract_object

    def get_contract_data(self, network_name, contract_name, abi_filename=None):
        data = None
        if network_name in self._artifact_items and contract_name in self._artifact_items[network_name]:
            logger.debug(f'found contract in library {network_name}.{contract_name}')
            data = self._artifact_items[network_name][contract_name]
        else:
            if abi_filename is None:
                abi_filename = f'{contract_name}.{network_name}.json'

            abi_filename_path = ContractManager.find_abi_filename(abi_filename)
            if abi_filename_path:
                logger.debug(f'loading contract from file at {abi_filename_path}')
                data = ContractManager.load_abi_file(abi_filename_path)
        return data

    def set_contract_data(self, network_name, contract_name, data):
        if network_name not in self._artifact_items:
            self._artifact_items[network_name] = {}
        self._artifact_items[network_name][contract_name] = data

    @property
    def web3(self):
        return self._web3

    @staticmethod
    def _find_class_in_module(class_name, contract_module):
        for name, obj in inspect.getmembers(contract_module, inspect.isclass):
            if issubclass(obj, ContractBase) \
               and name != 'ContractBase' \
               and name == class_name:
                return obj
        return None

    @staticmethod
    def find_abi_filename(filename):
        test_file = os.path.join(os.path.dirname(__file__), 'data', filename)
        if os.path.exists(test_file):
            return test_file

        test_file = os.path.join('artifacts', filename)
        if os.path.exists(test_file):
            return test_file
        return None

    @staticmethod
    def load_abi_file(filename):
        if filename and os.path.exists(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)

    @staticmethod
    def load_artifact_library(filename):
        data = None
        artifact_libray_file = os.path.join(os.path.dirname(__file__), 'data', filename)
        if os.path.exists(artifact_libray_file):
            with gzip.open(artifact_libray_file, 'rt') as fp:
                data = json.load(fp)
        return data
