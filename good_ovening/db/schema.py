#!/usr/bin/python
from collections import OrderedDict
from good_ovening.db.database import SQLiteDatabase

class Schema(object):
    """Defines a database table schema, including column names, types, and keys """
    
    def __init__(self, name):
        self.name = name
        self.columns = OrderedDict()
        self.primary_key = None

    def add_column(self, column, column_type, set_primary_key):
        """Insert a new column into this schema. Overwrite on duplicate name """
        self.columns[column] = column_type
        if set_primary_key:
            self.primary_key = column

    def get_columns(self):
        """return the list of column names for this schema """
        return self.columns.keys()
            
    def column_gen(self):
        """Generator expression return column names for this schema """
        for column in self.columns:
            yield column

    def get_column_type(self, column_name):
        """Return the column type for the given name """
        return self.columns[column_name]

    def get_primary_key(self):
        """Return the primary key """
        return self.primary_key

    def to_string(self):
        """Return a string representation of this schema """
        rows = ["%d | %s | %s" % (i, col, col_type) if col != self.primary_key else
                "%d | %s | %s | PRIMARY KEY" % (i, col, col_type) for i, (col, col_type)
                in enumerate(self.columns.iteritems())]
        schema_string = "\n".join(rows)
        return schema_string

def schema_from_db(database, table):
    """Return a schema object for the given table in the given database """
    schema = Schema(table)
    db = SQLiteDatabase.get_instance()
    for _, col, col_type, _, _, is_primary in db.get_table_info(database, table):
        schema.add_column(col, col_type, is_primary)
    return schema

def schema_from_ordered_dict(schema_dict, name):
    """Return a schema object with the columns and column types defined in
    the given OrderedDict """
    assert type(schema_dict) == OrderedDict, "Must supply an OrderedDict"
    schema = Schema(name)
    for col, col_type in schema_dict.iteritems():
        set_primary_key = False
        if "PRIMARY KEY" in col_type:
            col_type = col_type.split(" ")[0]
            set_primary_key = True
        schema.add_column(col, col_type, set_primary_key)
    return schema
