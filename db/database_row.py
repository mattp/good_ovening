#!/usr/bin/python

class DatabaseRow(object):
    """Simple container to store database row"""

    def __init__(self):
        self.items = {}
        
    def add_item(self, item_name, item):
        """Add an item to the dictionary (warn if exists)"""
        assert type(item_name) == str, "Item key must be type 'str'"
        if item_name in self.items:
            print("Warning: overwriting previous item for '%s'" % item_name)
        self.items[item_name] = item

    def get_item(self, item_name):
        """Return the given item, if it exists """
        assert type(item_name) == str, "Item key must be type 'str'"
        try:
            return self.items[item_name]
        except AttributeError, e:
            print("%s: %s" % (type(e).__name__, e))
            
class OvenDatabaseRow(DatabaseRow):
    """Immutable container to store and access extracted OVEN database row """

    def __init__(self, oven_item):
        super(OvenDatabaseRow, self).__init__()
        self.oven_item = oven_item
        
    def add_ad_id(self, ad_id):
        """Add a single 'ad_id' item """
        self.add_item("ad_id", ad_id)

    def get_ad_id(self):
        """Return the ad_id associated with this row """
        return self.get_item("ad_id")
