#!/usr/bin/python
import config as conf

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
    """Container to store and access extracted OVEN database row """
    
    def __init__(self):
        super(OvenDatabaseRow, self).__init__()
        
    def set_ad_id(self, ad_id):
        """Add a single ad id item """
        self.add_item(conf.AD_ID_KEY, ad_id)

    def get_ad_id(self):
        """Return the ad id associated with this row """
        return self.get_item(conf.AD_ID_KEY)        
        
    def set_ad_link(self, ad_link):
        """Add a single ad link item """
        self.add_item(conf.AD_LINK_KEY, ad_link)

    def get_ad_link(self):
        """Return the ad id associated with this row """
        return self.get_item(conf.AD_LINK_KEY)        

    def set_oven_type(self, oven_type):
        """Add a single ad link item """
        self.add_item(conf.OVEN_TYPE_KEY, oven_type)

    def get_oven_type(self):
        """Return the ad id associated with this row """
        return self.get_item(conf.OVEN_TYPE_KEY)        

    
    
