
#
# ATT 2017-05-03 v10.0.52 - New odoo Functions
# ATT 2017-04-26 v10.0.1
#
# TOOLS FOR ODOO 10+
#
# CUSTOM FUNCTIONS FOR XML IMPORT
#
 
import odoo_importer_from_xml_cxsd_config as config
import odoo_importer_from_xml_cxsd as importer
import sys
import random
import time
from datetime import datetime, timezone #Py3

def getMainId():
	return config.main_id

#Odoo
def getOdooUserId():
	return config.odooConfigDict["odoo_uid"]

def getOdooUserName():
	return config.odooConfigDict["odoo_username"]

def getCurrentDateTimeForSQL():
	return time.strftime('%Y-%m-%d %H:%M:%S')

def getXMLFilename():
	return config.inputXMLFileName

def getRandomNumber():
	return str(random.randint(0, sys.maxsize))

def getFormDateTime():
	return convertDateTimeFromEpochDateTime(config.formDateTime)

#Return Formatted Date from timestamp in miliseconds
def convertDateTimeFromEpochDateTime(datetime_from_epoch_ms):
	return datetime.fromtimestamp(int(datetime_from_epoch_ms)/1000, timezone.utc)

