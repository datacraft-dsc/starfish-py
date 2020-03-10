"""


    Contract Manager

    loads contracts


"""

import importlib
import inspect
import json
import logging
import os

from starfish.contract.contract_base import ContractBase

logger = logging.getLogger(__name__)


class ContractManager:

    def __init__(self, web3, default_package_name):
        self._web3 = web3
        self._default_package_name = default_package_name

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
        if abi_filename is None:
            abi_filename = f'{contract_name}.{network_name}.json'
        if abi_filename:
            abi_filename_path = ContractManager.find_abi_filename(abi_filename)
            if abi_filename_path:
                contract_info = ContractManager.load_abi_file(abi_filename_path)
                contract_object.load(self.web3, abi=contract_info['abi'], address=contract_info['address'])
            else:
                raise FileNotFoundError(f'Cannot find artifact file for contract {contract_name} {abi_filename}')
        else:
            # load in an dummy contract with no abi or address
            contract_object.load(self.web3)

        return contract_object

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
        test_file = os.path.join('artifacts', filename)
        if os.path.exists(test_file):
            return test_file
        return None

    @staticmethod
    def load_abi_file(filename):
        if filename and os.path.exists(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)
