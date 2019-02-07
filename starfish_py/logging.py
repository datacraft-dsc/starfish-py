"""
    Setup logging, this ideally must be called only once an the start of using
    this library.

"""

import os
import logging.config
import logging
import yaml
import coloredlogs


def setup_logging(level=logging.INFO, filename='logging.yaml', env_key='LOG_CFG'):
    """
    **@author:** Prathyush SP, but hacked around by Bill
    Logging Setup
    """
    value = os.getenv(env_key, None)
    if value:
        filename = value

    # start basic logging
    logging.basicConfig(level=level)
    coloredlogs.install(level=level)

    if os.path.exists(filename):
        with open(filename, 'rt') as file_handle:
            try:
                config = yaml.safe_load(file_handle.read())
                logging.config.dictConfig(config)
                logging.info(f'Logging configuration loaded from file: {filename}')
            except yaml.YAMLError as error_exception:
                print(error_exception)
                logging.error(f'Failed to load logging configuration file {filename}: {error_exception}')
