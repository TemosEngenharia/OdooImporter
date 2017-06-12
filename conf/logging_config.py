import os
import json
import logging.config

#ATT 2017-05-11
#
#Esse modulo nao requer personalizacao
# Use o arquivo logging.json para personalizar a configuracao.

#This module doesn't require any custom changes
# Use the file logginh.json for any customize on configuration.

def setup_logging(
    default_path='/etc/OdooImporter/logging_config.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
    ):
    #Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
