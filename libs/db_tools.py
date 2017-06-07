# ATT 2017-05-03 v10.0.52 - Database Insert Command execution

import psycopg2
from conf.db_config import db_config
 #Logging Required Imports
import conf.logging_config as lc
import logging

def updateDB(updateSQL):
    logger = logging.getLogger(__name__)
    conn = None
    inserted_id = None

    try:
        # read database configuration
        params = db_config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(updateSQL)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()


def insertInToDB(insertMainSQL):
    logger = logging.getLogger(__name__)
    conn = None
    inserted_id = None

    try:
        # read database configuration
        params = db_config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(insertMainSQL)
        # get the generated id back
        inserted_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
 
    return inserted_id

 

def deleteFromDB(deleteSQL):
    logger = logging.getLogger(__name__)
    conn = None
    inserted_id = None

    try:
        # read database configuration
        params = db_config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(deleteSQL)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()    



def insert_vendor_sample(vendor_name):
    logger = logging.getLogger(__name__)
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (vendor_name,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
 
    return vendor_id