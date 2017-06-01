# ATT 2017-05-03 v10.0.52 - New odoo Config Function
#!/usr/bin/python
#Logging Required Imports
import logging_config as lc
import logging

from configparser import ConfigParser
 
 
def db_config(filename='/etc/odoo-dev/db_config.ini', section='postgresql'):
    logger = logging.getLogger(__name__)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db


def odoo_config(filename='/etc/odoo-dev/db_config.ini', section='odoo'):
    logger = logging.getLogger(__name__)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
