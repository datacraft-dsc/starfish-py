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
    """
    Setup the contract manager to load and get contracts

    :param web3: Web3 connection to the block chain
    :param str network_name: name of the connected network
    :param str default_package_name: default package name for the contract module

    """

    def __init__(self, web3, network_name, default_package_name):
        self._web3 = web3
        self._network_name = network_name
        self._default_package_name = default_package_name
        self._artifact_items = ContractManager.load_artifact_library(ARTIFACT_DATA_FILENAME)
        if self._artifact_items is None:
            self._artifact_items = []

    def load(self, name, artifact_filename=None, has_artifact=None, package_name=None):
        """

        Load a contract using it's name, and network name

        :param str name: Name of the contract to load
        :param str artifact_filename: Optional filename of the artifact file
        :param bool has_artifact: Defaults to True, if false then just load the contract without an abi & address
        :param str package_name: Defaults to default_package_name, the package for the contract module

        :return: Return a contract object, else return None

        """
        if package_name is None:
            package_name = self._default_package_name
        if package_name is None:
            raise ValueError(f'You need to provide a package name for the contract classes')

        if has_artifact is None:
            has_artifact = True

        package_module = importlib.import_module(package_name)
        for item in inspect.getmembers(package_module, inspect.ismodule):
            class_def = ContractManager._find_class_in_module(name, item[1])
            if class_def:
                return self.create_contract_object(
                    name,
                    class_def,
                    artifact_filename=artifact_filename,
                    has_artifact=has_artifact
                )
        return None

    def create_contract_object(self, name, class_def, artifact_filename=None, has_artifact=None):
        """

        Create a new contract object from a class definition

        :param str name: Name of the contract
        :param class class_def: Class definition of the contract
        :param str artifact_filename: Optional filename of the artifact file
        :param bool has_artifact: Defaults to True, if false then just load the contract without an abi & address

        :return: Return a contract object, else return None

        """
        if has_artifact is None:
            has_artifact = True

        contract_object = class_def()
        contract_name = contract_object.name

        # only load in an artifact file if it is needed by the contract
        if has_artifact:
            contract_data = self.get_contract_data(contract_name, artifact_filename)
            if contract_data:
                contract_object.load(self.web3, abi=contract_data['abi'], address=contract_data['address'])
            else:
                raise FileNotFoundError(f'Cannot find artifact data for contract {contract_name}.{self._network_name}')
        else:
            # load in an dummy contract with no abi or address
            contract_object.load(self.web3)

        return contract_object

    def get_contract_data(self, name, artifact_filename=None):
        """

        Get the contract article data from a file or from the library.

        :param str name: Name of the contract
        :param str artifact_filename: Optional filename of the artifact file

        :return: Return a contract article data or None

        """
        data = None
        if self._network_name in self._artifact_items and name in self._artifact_items[self._network_name]:
            logger.debug(f'found contract in library {name}.{self._network_name}')
            data = self._artifact_items[self._network_name][name]
        else:
            if artifact_filename is None:
                artifact_filename = f'{name}.{self._network_name}.json'

            artifact_filename_path = ContractManager.find_artifact_filename(artifact_filename)
            if artifact_filename_path:
                logger.debug(f'loading contract artifact file at {artifact_filename_path}')
                data = ContractManager.load_artifact_file(artifact_filename_path)
        return data

    def set_contract_data(self, name, data):
        """

        Set the contract article data for given contract.

        :param str name: Name of the contract to set
        :param dict data: Article data for the contract

        """
        if self._network_name not in self._artifact_items:
            self._artifact_items[self._network_name] = {}
        self._artifact_items[self._network_name][name] = data

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
    def find_artifact_filename(filename):
        test_file = os.path.join(os.path.dirname(__file__), 'data', filename)
        if os.path.exists(test_file):
            return test_file

        test_file = os.path.join('artifacts', filename)
        if os.path.exists(test_file):
            return test_file
        return None

    @staticmethod
    def load_artifact_file(filename):
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
