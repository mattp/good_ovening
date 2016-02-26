#!/usr/bin/python
from optparse import OptionParser
import good_ovening.config as conf
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
        assert v_origin in conf.VERSION_SCHEMAS, "Invalid origin version %r" % v_origin
        assert v_dest in conf.VERSION_SCHEMAS, "Invalid destination version %r" % v_dest
        orig_schemas = conf.VERSION_SCHEMAS[v_origin]
        dest_schemas = conf.VERSION_SCHEMAS[v_dest]
        for orig_schema, dest_schema in zip(orig_schemas, dest_schemas):
            remove_cols = self._get_remove_columns(orig_schema, dest_schema)

    def remove_columns(self, database, table, remove_cols):
        """Remove the given columns from the given table in the given database """
        pass
        
    def _get_remove_columns(self, orig_schema, dest_schema):
        """Get the list of columns that are totally removed during migration """
        assert type(orig_schema) == OrderedDict, "Origin schema must be an OrderedDict, " \
            "found '%r'" % type(orig_schema)
        assert type(dest_schema) == OrderedDict, "Destination schema must be an OrderedDict, " \
            "found '%r'" % type(dest_schema)
        remove_cols = [col for col in orig_schema if col not in dest_schema and
                       (col not in conf.COLUMN_UPDATES
                        or conf.COLUMN_UPDATES[col] != dest_schema)]
        return remove_cols

    def _get_change_columns(self, orig_schema, dest_schema):
        """Get the list of columns that are changed during migration """
        assert type(orig_schema) == OrderedDict, "Origin schema must be an OrderedDict, " \
            "found '%r'" % type(orig_schema)
        assert type(dest_schema) == OrderedDict, "Destination schema must be an OrderedDict, " \
            "found '%r'" % type(dest_schema)
        change_cols = [col for col in orig_schema if col in conf.COLUMN_UPDATES]
        return change_cols

    def _get_add_columns(self, orig_schema, dest_schema):
        """Get the list of columns are added during migration """
        assert type(orig_schema) == OrderedDict, "Origin schema must be an OrderedDict, " \
            "found '%r'" % type(orig_schema)
        assert type(dest_schema) == OrderedDict, "Destination schema must be an OrderedDict, " \
            "found '%r'" % type(dest_schema)
        add_cols = [col for col in dest_schema if col not in orig_schema]
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

    

    
