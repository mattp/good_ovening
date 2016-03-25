#!/usr/bin/python
from good_ovening.singleton import Singleton
from abc import ABCMeta, abstractmethod
import sqlite3

class Database():
    """Base for all Database connection classes, includes abstract definitions for getting
    connections, executing queries, returning results, etc. """
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_query(self):
        pass

    @abstractmethod
    def remove_column(self):
        pass

    @abstractmethod
    def clear_table(self):
        pass
    
    @abstractmethod
    def drop_table(self):
        pass
    
    @abstractmethod
    def get_table_info(self):
        pass
    
@Singleton    
class SQLiteDatabase(Database):
    """SQLite implementation of Database class """

    conn = None
    
    def __init__(self):
        pass
        
    def _open_connection(self, database):
        """Connect to the SQLite database (if not cached) and return the
        cursor object. Handle any connection errors. """
        self.conn = sqlite3.connect(database)
        return self.conn.cursor()

    def _close_connection(self):
        """Commit any outstanding transactions and close the current
        connection """
        if self.conn:
            self.conn.commit()
            self.conn.close()
        
    def execute_query(self, database, query):
        """Execute the supplied query on the given database, return any
        results, and handle any errors """
        cursor = self._open_connection(database)
        res = list(cursor.execute(query))
        self._close_connection()
        return res

    def remove_column(self, database, table, col):
        """Remove a single column from the database schema """
        columns = [c for _, c, _, _, _, _ in
                   self.get_table_info(database, table) if c != col]
        col_select_str = ", ".join(columns)
        queries = ["CREATE TABLE %s_backup(%s)" % (table, col_select_str),
                   "INSERT INTO %s_backup SELECT %s FROM %s" % (table, col_select_str, table),
                   "DROP TABLE %s" % table,
                   "CREATE TABLE %s(%s)" % (table, col_select_str),
                   "INSERT INTO %s SELECT %s FROM %s_backup" % (table, col_select_str, table),
                   "DROP TABLE %s_backup" % table]
        try:
            for query in queries:
                self.execute_query(database, query)
        except sqlite3.OperationalError, e:
            print(e)

    def clear_table(self, database, table):
        """Clear the data in the given SQLite table """
        query = "DELETE FROM %s" % table
        self.execute_query(database, query)
            
    def drop_table(self, database, table):
        """Drop a table from the given database """
        self.clear_table(database, table)
        query = "DROP TABLE %s" % table
        self.execute_query(database, query)
            
    def get_table_info(self, database, table):
        """Return the schema for a given table in the given database """
        query = "PRAGMA TABLE_INFO(%s)" % table
        res = self.execute_query(database, query)
        return res
        
    
