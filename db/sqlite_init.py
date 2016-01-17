#!/usr/bin/python
import config as conf
import sqlite3
from database import SQLiteDatabase

if __name__=="__main__":

    db = SQLiteDatabase.get_instance()
    init_query = """ 
    CREATE TABLE %s (ad_id INTEGER PRIMARY KEY, link varchar(250),
    oven_type varchar(20), latitude varchar(10), longitude
    varchar(10)) """ % conf.LISTINGS_TABLE
    try:
        db.execute_query(conf.DB_PATH, init_query)
    except sqlite3.OperationalError, e:
        print(e)
