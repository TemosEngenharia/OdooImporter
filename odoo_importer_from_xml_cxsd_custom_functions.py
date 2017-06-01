
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

def getSQLDateTimeFromJoinedStringInternational(joined_datetime_string):

    if len(joined_datetime_string) == 12:

        dt = datetime.strptime(joined_datetime_string, "%Y%m%d%H%M")
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    elif len(joined_datetime_string) == 14:

        dt = datetime.strptime(joined_datetime_string, "%Y%m%d%H%M%S")
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    else:
        return ""


def getSQLDateTimeFromJoinedStringBrazilian(joined_datetime_string):
    logger = logging.getLogger(__name__)

    if len(joined_datetime_string) == 12:

        dt = datetime.strptime(joined_datetime_string, "%d%m%Y%H%M")
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    elif len(joined_datetime_string) == 14:

        dt = datetime.strptime(joined_datetime_string, "%d%m%Y%H%M%S")
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    else:

        return ""

def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)


#Returns delta time between two dates.
def getDeltaTimeBrazilianDateTimeStrings(old_date_time_joined_string, new_date_time_joined_string):
    logger = logging.getLogger(__name__)

    dateTimeStringOld = getSQLDateTimeFromJoinedStringBrazilian(old_date_time_joined_string)
    dateTimeStringNew = getSQLDateTimeFromJoinedStringBrazilian(new_date_time_joined_string)
    
    #logger.info(dateTimeStringOld)
    #logger.info(dateTimeStringNew)
    
    dateTimeOld = datetime.strptime(dateTimeStringOld, '%Y-%m-%d %H:%M:%S')
    dateTimeNew = datetime.strptime(dateTimeStringNew, '%Y-%m-%d %H:%M:%S')
  
    logger.info(dateTimeOld)
    logger.info(dateTimeNew)
  
    logger.info(dateTimeNew-dateTimeOld)

    if dateTimeNew>dateTimeOld:

        elapsedTime = dateTimeNew-dateTimeOld

        d =  divmod(elapsedTime.total_seconds(), 86400) #days
        h = divmod(d[1],3600)  # hours
        m = divmod(h[1],60)  # minutes
        s = m[1]  # seconds

        return '%d dias, %d horas, %d minutos e %d segundos' % (d[0],h[0],m[0],s)

    else:
        return ""


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

    if prefix in ["MCO20"]:
      return 'MCO20-dev.cxsd'

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

    if prefix in ["COR31"]:
      return 'COR31.cxsd'

    return "COR27" #default