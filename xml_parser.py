#!/usr/bin/python
import xml.etree.ElementTree
import config as conf

class XMLParser():

    tree = None
    root = None
    
    def load_file(self, filepath):
        """Load an XML object from the given filepath"""
        try:
            self.tree = xml.etree.ElementTree.parse(filepath)
            self.root = self.tree.getroot()
        except IOError, e:
            print(e)

    def img_src_generator(self):
        """Yield available image sources from XML """
        for s in self.root.findall(conf.IMG_SRC_XPATH):
            yield s.text
        
