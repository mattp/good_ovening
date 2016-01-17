#!/usr/bin/python
from singleton import Singleton
from abc import ABCMeta, abstractmethod
import sqlite3

class Database():
    """Base for all Database connection classes, includes abstract definitions for getting
    connections, executing queries, returning results, etc. """
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_query(self):
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
        res = cursor.execute(query)
        self._close_connection()
        return res

if __name__=="__main__":
    db = SQLiteDatabase.get_instance()
    
    
