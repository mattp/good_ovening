#!/usr/bin/python
import good_ovening.config as conf
import sqlite3
from good_ovening.db.database import SQLiteDatabase

def clear_table(database, table):
    """Clear the data in the given SQLite table """
    db = SQLiteDatabase.get_instance()
    query = "DELETE FROM %s" % table
    db.execute_query(database, query)

def init_listings_table(database):
    """Initialize a table for storing listings data, using the given table
    name """
    db = SQLiteDatabase.get_instance()
    init_query = """ 
    CREATE TABLE %s (ad_id INTEGER PRIMARY KEY, link varchar(250),
    oven_type varchar(20), latitude varchar(10), longitude
    varchar(10)) """ % conf.LISTINGS_TABLE
    try:
        db.execute_query(database, init_query)
    except sqlite3.OperationalError, e:
        print("Database already exists. Skipping.")
    
if __name__=="__main__":
    init_listings_table(conf.DB_PATH)
