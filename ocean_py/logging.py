import yaml
import os
import logging.config
import logging
import coloredlogs


def setup_logging(level=logging.INFO, setup_file='logging.yaml', env_key='LOG_CFG'):
    """
    | **@author:** Prathyush SP
    | Logging Setup
    """
    value = os.getenv(env_key, None)
    if value:
        setup_file = value
    if os.path.exists(setup_file):
        with open(setup_file, 'rt') as file_handle:
            try:
                config = yaml.safe_load(file_handle.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
                logging.info("Logging configuration loaded from file: {}".format(path))
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=level)
                coloredlogs.install(level=level)
    else:
        logging.basicConfig(level=level)
        coloredlogs.install(level=level)
        # print('Failed to load configuration file. Using default configs')
