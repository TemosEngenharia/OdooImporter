
#
# ATT 2017-05-03 v10.0.52 - New odoo Functions
# ATT 2017-04-26 v10.0.1
#
# TOOLS FOR ODOO 10+
#
# CUSTOM FUNCTIONS FOR XML IMPORT
#
 #Logging Required Imports
import logging_config as lc
import logging

import odoo_importer_from_xml_cxsd_config as config
import odoo_importer_from_xml_cxsd as importer
import sys
import random
import time
from datetime import datetime, timezone #Py3

def getMainId():
    logger = logging.getLogger(__name__)
    return config.main_id

#Odoo
def getOdooUserId():
    logger = logging.getLogger(__name__)
    return config.odooConfigDict["odoo_uid"]

def getOdooUserName():
    logger = logging.getLogger(__name__)
    return config.odooConfigDict["odoo_username"]

def getCurrentDateTimeForSQL():
    logger = logging.getLogger(__name__)
    return time.strftime('%Y-%m-%d %H:%M:%S')

def getXMLFilename():
    logger = logging.getLogger(__name__)
    return config.inputXMLFileName

def getRandomNumber():
    logger = logging.getLogger(__name__)
    return str(random.randint(0, sys.maxsize))

def getFormDateTime():
    logger = logging.getLogger(__name__)
    return convertDateTimeFromEpochDateTime(config.formDateTime)

#Return Formatted Date from timestamp in miliseconds
def convertDateTimeFromEpochDateTime(datetime_from_epoch_ms):
    logger = logging.getLogger(__name__)
    return datetime.fromtimestamp(int(datetime_from_epoch_ms)/1000, timezone.utc)

#Config of Custom Schemas based on prefix of file (5Chars)
def getSchemaFilenameForPrefix(prefix):
    logger = logging.getLogger(__name__)

    if prefix in ["COR9_"]:
      return 'COR09.cxsd'

    if prefix in ["COR16"]:
      return 'COR16.cxsd'

    if prefix in ["COR17", "COR18", "COR19", "COR19"]:
      return 'COR19.cxsd'   

    if prefix in ["COR20", "COR21", "COR22"]:
      return 'COR20.cxsd'

    if prefix in ["COR23"]:
      return 'COR23.cxsd'

    if prefix in ["COR24"]:
      return 'COR24.cxsd'

    if prefix in ["COR25"]:
      return 'COR25.cxsd'

    if prefix in ["COR27"]:
      return 'COR27.cxsd'

    if prefix in ["COR28", "COR29", "COR30"]:
      return 'COR27.cxsd'

    return "COR27" #default