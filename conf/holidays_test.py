#!/usr/bin/env python
# -*- coding uft-8 -*-
import logging_config as lc
import logging


import holiday_config as holiday


#---------------------------------------------------
def main():
    #Load Logging Default Config
    lc.setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("----- -> START_UP <- "+"-"*50)

    #Init Holiday Class
    holiday.init("START HOLIDAY CONFIG LOADER")

    date_for_test = "2017-06-11"

    #1
    logger.info(holiday.holidays)
    
    #2
    logger.info(holiday.holidays[3])
    
    #3
    logger.info('is_sunday("{}")? [{}]'.format(date_for_test, holiday.is_sunday(date_for_test)))
    
    #4
    logger.info('is_holiday("{}")? [{}]'.format(date_for_test, holiday.is_holiday(date_for_test)))
    
    #5
    logger.info('is_work_day_off("{}")? [{}]'.format(date_for_test, holiday.is_work_day_off(date_for_test)))


    print("END OF TESTS")


#---------------------------------------------------
if __name__ == "__main__":
    main()
