import os
import json

 #Logging Required Imports
import logging_config as lc
import logging
from datetime import datetime

#ATT 2017-06-12
# Config Handler for Holidays. requires:holidays.json
#
# Esse modulo nao requer personalizacao
# Use o arquivo logging.json para personalizar a configuracao.

# This module doesn't require any custom changes
# Use the file logginh.json for any customize on configuration.


def setup_holiday(default_path='/etc/OdooImporter/holidays.json'):
    logger = logging.getLogger(__name__)

    path = default_path

    try:
        if os.path.exists(path):
            with open(path, 'rt') as f:

                holidays = json.load(f)
                #print(holidays)
                return holidays


    except Exception as e:
        logger.error("Problem: File not found:" + default_path + " | " + str(e))
        return None       


#Check if is holiday
def is_holiday(dateValue):
    logger = logging.getLogger(__name__)
    
    try:
        date = datetime.strptime(dateValue, "%Y-%m-%d")

        if len(holidays)>0:

            if len(search_for(dateValue, 'holiday_usformat_date', holidays))>0:

                return True
            else:
                return False
        else:
            return False

    except ValueError as e:
        logger.error(str(e))
        return False        


#Check if is sunday
def is_sunday(dateValue):
    logger = logging.getLogger(__name__)
    try:
        cur_date = datetime.strptime(dateValue, "%Y-%m-%d")
        cur_weekday = cur_date.weekday()

        #logger.info(cur_date.weekday())

        if cur_weekday==6:
            return True
        else:
            return False

    except ValueError as e:
        logger.error(str(e))
        return False        


#Check if is_work_day_off (Validate if is Sunday and/or Holiday)
def is_work_day_off(dateValue):
    logger = logging.getLogger(__name__)

    
    if is_holiday(dateValue)==True or is_sunday(dateValue)==True:
        return True
    else:
        return False


#function for search a text in list of dictionaries
def search_for(name, name_id, list):
    return [element for element in list if element[name_id] == name]


def init(arg="HOLIDAY INIT"):
  logger = logging.getLogger(__name__)
  #logger.info(str(arg))


  global holidays
  holidays = setup_holiday()
