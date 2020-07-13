"""


    Local node Utils to get local node artifact files, from a docker container


"""

import json
import logging
import os
import re
import tarfile
import tempfile
from typing import Any
import docker


logger = logging.getLogger(__name__)


def get_local_contract_files(docker_name: str, from_folder: str) -> Any:
    items = []
    client = docker.from_env()
    container_list = client.containers.list(filters={'name': 'keeper-contracts'})
    if container_list:
        container = container_list[0]
        logger.debug(f'found container id: {container.id} name: {container.name} state: {container.status}')
        items = export_docker_contract_items(container, from_folder)
    return items


def export_docker_contract_items(container: Any, from_folder: str) -> Any:
    items = {}
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
                    if tar_item.isfile() and re.search(r'\.json$', tar_item.name):
                        filename = os.path.basename(tar_item.name)
                        # logger.debug(f'reading contract file {filename}, {tar_item.size}')
                        with tar.extractfile(tar_item) as fp:
                            contract_data = json.load(fp)
                            items[filename] = contract_data
                    tar_item = tar.next()
    return items
