"""


    Local node Utils to get local node artifact files, from a docker container


"""

import docker
import logging
import os
import tarfile
import re
import tempfile
import json


logger = logging.getLogger(__name__)


def get_local_contract_files(docker_name, network_names):
    items = []
    client = docker.from_env()
    container_list = client.containers.list(filters={'name': 'keeper-contracts'})
    if container_list:
        container = container_list[0]
        logger.debug(f'found container id: {container.id} name: {container.name} state: {container.status}')
        items = export_docker_contract_items(container, '/keeper-contracts/artifacts', network_names)
    return items

def is_file_name_valid(name, network_names):
    match = re.match(f'.*\S(\w+)\.(\w+)\.json', name, re.IGNORECASE)
    if match:
        return match.group(2) in network_names
    return False

def export_docker_contract_items(container, from_folder, network_names):
    items = []
    data, stat = container.get_archive(from_folder)
    if stat:
        with tempfile.TemporaryFile() as file_handle:
            for chunk in data:
                file_handle.write(chunk)
            file_handle.seek(0, 0)
            tar = tarfile.open(fileobj=file_handle)
            if tar:
                tar_item = tar.next()
                while tar_item:
                    if tar_item.isfile() and is_file_name_valid(tar_item.name, network_names):
                        logger.debug(f'contract file {tar_item.name}, {tar_item.size}')
                        with tar.extractfile(tar_item) as fp:
                            contract_data = json.load(fp)
                            items.append(contract_data)
                    tar_item = tar.next()
    return items