#!/usr/bin/python
import good_ovening.config as conf
import sqlite3
from good_ovening.db.database import SQLiteDatabase


def init_listings_table(database):
    """Initialize a table for storing listings data, using the given table name """
    db = SQLiteDatabase.get_instance()
    cols = ",".join(["%s %s" % (key, val) for key, val in conf.LISTINGS_SCHEMA.iteritems()])
    init_query = "CREATE TABLE %s (%s)" % (conf.LISTINGS_TABLE, cols)
    try:
        db.execute_query(database, init_query)
    except sqlite3.OperationalError, e:
        # update_listings_rows(database)
        print("Database already exists. Skipping.")
        
# def update_listings_rows(database):
#     """Ensure the correct rows are present in the listings table and, if
#     not, update """
#     db = SQLiteDatabase.get_instance()
#     schema_query = "PRAGMA TABLE_INFO(%s)" % conf.LISTINGS_TABLE
#     res = [col for _, col, _, _, _, _ in  db.execute_query(database, schema_query)]
#     missing_cols = [col for col in conf.LISTINGS_SCHEMA.keys() if col not in res]
#     for col in missing_cols:
#         alter_query = "ALTER TABLE %s ADD COLUMN %s %s" \
#                       % (conf.LISTINGS_TABLE, col, conf.LISTINGS_SCHEMA[col])
#         print(alter_query)
#         db.execute_query(database, alter_query)

if __name__=="__main__":
    init_listings_table(conf.DB_PATH)
