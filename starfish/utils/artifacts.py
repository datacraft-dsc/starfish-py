
import logging
import os
import re
import sys

logger = logging.getLogger('starfish.artifacts')


def is_contract_type_exists(network_name, path):
    for filename in os.listdir(path):
        if re.match(fr'\w+\.{network_name}\.json', filename):
            return True
    return False


def find_contract_path(network_name):
    folder = os.path.abspath('artifacts')
    # first search the working folder of the app
    logger.debug(f'search for artifacts {folder}')
    if os.path.exists(folder):
        if is_contract_type_exists(network_name, folder):
            return folder
    logger.debug(f'search for artifacts {folder}')
    folder = os.path.join(sys.prefix, 'artifacts')
    if os.path.exists(folder):
        if is_contract_type_exists(network_name, folder):
            return folder

    logger.debug(f'artifacts not found')
    return None
