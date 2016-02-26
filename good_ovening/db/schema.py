#!/usr/bin/python
from collections import OrderedDict

class Schema(object):
    """Defines a database table schema, including column names, types, and keys """
    
    def __init__(self):
        pass

    def get_columns(self):
        pass

    def get_column_type(self, column_name):
        pass

    def get_primary_key(self):
        pass

    def to_string(self):
        pass

def schema_from_db(database, table):
    """Return a schema object for the given table in the given database """
    pass

def schema_from_ordered_dict(schema_dict):
    """Return a schema object with the columns and column types defined in
    the given OrderedDict """
    assert type(schema_dict) == OrderedDict, "Must supply an OrderedDict"
    
