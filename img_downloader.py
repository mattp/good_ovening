#!/usr/bin/python
import sys
import os
import urllib2
from xml_parser import XMLParser

class IMGDownloader():
    """Object that handles downloading and storing images from the web to disk """
    
    def download_img(self, url, output):
        """Attempt to download an image from the given URL and write to output """
        try:
            print("Downloading from: %s" % url)
            with open(output, 'wb') as f:
                f.write(urllib2.urlopen(url).read())
        except IOError, e:
            print(e)


if __name__=="__main__":
    script, data_xml = sys.argv
    xml_parser = XMLParser()
    xml_parser.load_file(data_xml)
    downloader = IMGDownloader()
    if not os.path.exists("./img"):
        os.makedirs("./img", 0755)
    [downloader.download_img(src, "img/img_%d.jpg" % i)
     for i, src in enumerate(xml_parser.img_src_generator())]
