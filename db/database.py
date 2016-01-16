#!/usr/bin/python
from abc import ABCMeta, abstractmethod
from singleton import Singleton
import sqlite3

class Database():
    """Base for all Database connection classes, includes abstract definitions for getting
    connections, executing queries, returning results, etc. """
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def execute_query(self):
        pass

@Singleton    
class SQLiteDatabase(Database):
    """SQLite implementation of Database class """

    def __init__(self):
        print("SQLiteDatabase created")
    
    def _get_connection(self):
        """Connect to the SQLite database and return the connection
        object. Handle any connection errors. """
        conn = sqlite3.connect('test.db')
        return conn
        
    def execute_query(self, query):
        pass
    

if __name__=="__main__":
    db = SQLiteDatabase.get_instance()
    
    
