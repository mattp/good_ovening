#!/usr/bin/python
from optparse import OptionParser
import good_ovening.config as conf
import good_ovening.db.schema as schema
from good_ovening.db.database import SQLiteDatabase
from collections import OrderedDict

parser = OptionParser()
parser.add_option("-v", "--version", dest="version", type="string",
                  help="[Required] Version of database to migrate to.")
parser.add_option("-o", "--origin", dest="origin", type="string",
                  help="[Required] Version to migrate from.")

class MigrationHandler(object):
    """Handle database migration between various deployments of good_ovening """
    
    def migrate_db(self, database, v_origin, v_dest):
        """Map the good_ovening database from the origin to destination versions """
        assert v_origin in conf.VERSION_CONFIGS, "Invalid origin version %r" % v_origin
        assert v_dest in conf.VERSION_CONFIGS, "Invalid destination version %r" % v_dest
        orig_version_config = conf.VERSION_CONFIGS[v_origin]
        dest_version_config = conf.VERSION_CONFIGS[v_dest]
        # Handle pre-existing tables
        for table in orig_version_config.schema_name_gen():
            orig_schema_dict = orig_version_config.get_schema_dict(table)
            orig_schema = schema.schema_from_ordered_dict(orig_schema_dict, v_origin)
            if dest_version_config.has_schema(table):
                dest_schema_dict = dest_version_config.get_schema_dict(table)
                dest_schema = schema.schema_from_ordered_dict(dest_schema_dict, v_dest)
                remove_cols = self._get_remove_columns(orig_schema, dest_schema)
                self.remove_columns(database, table, remove_cols)
                add_cols = self._get_add_columns(orig_schema, dest_schema)
                self.add_columns(database, table, add_cols)
                change_cols = self._get_change_columns(orig_schema, dest_schema)
                self.change_columns(database, table, change_cols)
            else:
                self.drop_table(database, table)
        # Handle new tables
        new_tables = [name for name in dest_version_config.schema_name_gen()
                      if not orig_version_config.has_schema(name)]
        for table in new_tables:
            self.add_table(database, table)
                
    def drop_table(self, database, table):
        """Remove the given table from the given database completely """
        db = SQLiteDatabase.get_instance()
        db.drop_table(database, table)
                
    def remove_columns(self, database, table, remove_cols):
        """Remove the given columns from the given table in the given database """
        db = SQLiteDatabase.get_instance()
        for col in remove_cols:
            db.remove_column(database, table, col)
        
    def _get_remove_columns(self, orig_schema, dest_schema):
        """Get the list of columns that are totally removed during migration """
        assert type(orig_schema) == schema.Schema, "Origin schema must be type Schema, " \
            "found '%r'" % type(orig_schema)
        assert type(dest_schema) == schema.Schema, "Destination schema be type Schema, " \
            "found '%r'" % type(dest_schema)
        dest_columns = dest_schema.get_columns()
        remove_cols = [col for col in orig_schema.column_gen() if col not in dest_columns and
                       (col not in conf.COLUMN_UPDATES or
                        conf.COLUMN_UPDATES[col] != dest_schema)]
        return remove_cols

    def _get_change_columns(self, orig_schema, dest_schema):
        """Get the list of columns that are changed during migration """
        assert type(orig_schema) == schema.Schema, "Origin schema must be type Schema, " \
            "found '%r'" % type(orig_schema)
        assert type(dest_schema) == schema.Schema, "Destination schema be type Schema, " \
            "found '%r'" % type(dest_schema)
        change_cols = [col for col in orig_schema.column_gen()
                       if col in conf.COLUMN_UPDATES]
        return change_cols

    def _get_add_columns(self, orig_schema, dest_schema):
        """Get the list of columns are added during migration """
        assert type(orig_schema) == schema.Schema, "Origin schema must be type Schema, " \
            "found '%r'" % type(orig_schema)
        assert type(dest_schema) == schema.Schema, "Destination schema be type Schema, " \
            "found '%r'" % type(dest_schema)
        orig_cols = orig_schema.get_columns()
        add_cols = [col for col in dest_schema.column_gen() if col not in orig_cols]
        return add_cols
        
def update_ref_link(self):
    """Update the values in the ref_link column (listings table) to origin_page values 
    and change the column name"""
    pass

if __name__=="__main__":

    # Handle commandline args
    (opts, args) = parser.parse_args()
    if not opts.version and opts.origin:
        parser.error("Migration origin and target required (-o and -v)")

    

    
