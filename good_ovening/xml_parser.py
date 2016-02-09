#!/usr/bin/python
import xml.etree.ElementTree as e_tree
import good_ovening.config as conf

class XMLParser(object):
    """Simple class for loading/storing an XML object from file"""

    def __init__(self):
        self.tree = None
        self.root = None
    
    def load_file(self, filepath):
        """Load an XML object from the given filepath"""
        try:
            self.tree = e_tree.parse(filepath)
            self.root = self.tree.getroot()
        except (IOError, e_tree.ParseError, TypeError), e:
            print("%s: %s" % (type(e).__name__, e))

    def xml_loaded(self):
        """Return whether or not this parser has an XML object currently
        loaded from file """
        return self.tree != None

class OvenXMLParser(XMLParser):
    """Sub-class of XMLParser, that handles specific operations to do with
    extracting data from the XML output of the good_ovening scraper """

    def __init__(self):
        super(OvenXMLParser, self).__init__()

    def img_src_generator(self):
        """Yield available image sources from XML """
        for s in self.root.findall(conf.IMG_SRC_XPATH):
            yield s.text

    def item_generator(self):
        """Yield item elements from the XML """
        for item in self.root.findall("item"):
            yield item
        
