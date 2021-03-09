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
import time
from typing import (
    Any,
    Generic
)
from urllib.parse import urljoin
import requests

from starfish.network.ethereum.contract.contract_base import ContractBase
from starfish.network.ethereum.ethereum_network import EthereumNetwork
from starfish.types import (
    TContractBase,
    TContractManager,
    TNetworkBase
)

logger = logging.getLogger(__name__)


ARTIFACT_DATA_FILENAME = 'artifacts.json.gz'
LOCAL_ARTIFACT_PACKAGE_SERVER = 'http://localhost:8550'


class ContractManager(Generic[TContractManager]):
    """
    Setup the contract manager to load and get contracts

    :param network: Network connection to the block chain
    :param str default_package_name: default package name for the contract module

    """

    def __init__(self, network: EthereumNetwork, default_package_name: str, artifacts_path: str) -> None:
        self._network = network
        self._default_package_name = default_package_name
        self._artifacts_path = artifacts_path
        self._artifact_items = ContractManager.load_artifacts_package(ARTIFACT_DATA_FILENAME)
        if self._artifact_items is None:
            self._artifact_items = []

    def load(self, name: str, artifact_filename: str = None, has_artifact: bool = None, package_name: str = None) -> TContractBase:
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
            raise ValueError('You need to provide a package name for the contract classes')

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

    def load_local_artifacts_package(self, url: str = None, timeoutSeconds: int = 20) -> None:
        if not url:
            url = LOCAL_ARTIFACT_PACKAGE_SERVER

        timeout = time.time() + timeoutSeconds
        info = self._request_local_artifacts_package(url)
        while not info and timeout < time.time():
            time.sleep(1)
            info = self._request_local_artifacts_package(url)
        if info and 'artifacts' in info:
            self._artifact_items = info['artifacts']

    def create_contract_object(self, name: str, class_def: Any, artifact_filename: str = None, has_artifact: bool = None) -> Any:
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
                contract_object.load(self._network.web3, abi=contract_data['abi'], address=contract_data['address'])
            else:
                raise FileNotFoundError(f'Cannot find artifact data for contract {contract_name}.{self._network.name}')
        else:
            # load in an dummy contract with no abi or address
            contract_object.load(self._network.web3)

        return contract_object

    def get_contract_data(self, name: str, artifact_filename: str = None) -> Any:
        """

        Get the contract article data from a file or from the library.

        :param str name: Name of the contract
        :param str artifact_filename: Optional filename of the artifact file

        :return: Return a contract article data or None

        """
        data = None

        # setup the default artifact filename
        if artifact_filename is None:
            artifact_filename = f'{name}.{self._network.network_id}.json'

        # first look for user defined folder for any artifact file
        artifacts_path_list = [self._artifacts_path, ContractManager.data_path()]
        artifact_filename_path = ContractManager.find_artifact_filename(artifact_filename, artifacts_path_list)
        if artifact_filename_path:
            logger.debug(f'loading contract artifact file at {artifact_filename_path}')
            data = ContractManager.load_artifact_file(artifact_filename_path)
        else:
            # now try to load from the artifact library
            if (str(self._network.network_id) in self._artifact_items and
                    name in self._artifact_items[str(self._network.network_id)]):
                logger.debug(f'found contract in library {name}.{self._network.network_id}')
                data = self._artifact_items[str(self._network.network_id)][name]

        return data

    def set_contract_data(self, name: str, data: Any) -> None:
        """

        Set the contract article data for given contract.

        :param str name: Name of the contract to set
        :param dict data: Article data for the contract

        """
        if self._network.network_id not in self._artifact_items:
            self._artifact_items[self._network.network_id] = {}
        self._artifact_items[self._network.network_id][name] = data

    def _request_local_artifacts_package(self, url: str) -> Any:
        """
        Request the artifacts package from the local package serever.
        This only works for local testing with a local private network.

        Usually the artifacts are stored in a single gzipped json file for all
        of the public and test block chain networks.
        :param str url: URL of the package server to request
        :returns: a dict on artifacts
        """
        data = None
        url = urljoin(f'{url}/', 'artifacts')
        logger.debug(f'requesting artifacts at url {url}')
        response = requests.get(url)
        if response and response.status_code == requests.codes.ok:
            data = response.json()
        return data

    @property
    def network(self) -> TNetworkBase:
        return self._network

    @property
    def artifacts_path(self) -> str:
        return self._artifacts_path

    @staticmethod
    def data_path() -> str:
        return os.path.join(os.path.dirname(__file__), 'data')

    @staticmethod
    def _find_class_in_module(class_name: str, contract_module: str) -> Any:
        for name, obj in inspect.getmembers(contract_module, inspect.isclass):
            if issubclass(obj, ContractBase) \
               and name != 'ContractBase' \
               and name == class_name:
                return obj
        return None

    @staticmethod
    def find_artifact_filename(filename: str, path_list: str) -> str:
        found_file = None
        for path in path_list:
            test_file = os.path.join(path, filename)
            if os.path.exists(test_file):
                found_file = test_file
                break

        return found_file

    @staticmethod
    def load_artifact_file(filename: str) -> Any:
        if filename and os.path.exists(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)

    @staticmethod
    def load_artifacts_package(filename: str) -> Any:
        data = None
        artifact_libray_file = os.path.join(ContractManager.data_path(), filename)
        if os.path.exists(artifact_libray_file):
            with gzip.open(artifact_libray_file, 'rt') as fp:
                data = json.load(fp)
        return data
