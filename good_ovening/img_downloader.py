#!/usr/bin/python
import sys
import os
import urllib2
import ntpath
import good_ovening.config as conf
from good_ovening.xml_parser import OvenXMLParser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="input_file", type="string",
                  help="[Required] Path to input data file in XML format")
parser.add_option("-o", "--output", dest="img_dir", type="string", default="./img",
                  help="[Required] Path to output directory where images are stored")

class IMGDownloader():
    """Object that handles downloading and storing images from the web to disk """
    
    def download_img(self, url, output):
        """Attempt to download an image from the given URL and write to output """
        try:
            print("Downloading from: %s" % url)
            with open(output, 'wb') as f:
                f.write(urllib2.urlopen(url).read())
            print("Wrote to: %s" % output)
        except IOError, e:
            print(e)


def download(input_file, img_dir):
    """Download all images in the supplied input file (XML format) and
    save them to the given output_dir (stored by AD ID)"""
    xml_parser = OvenXMLParser()
    xml_parser.load_file(opts.input_file)
    downloader = IMGDownloader()
    for item in xml_parser.item_generator():
        ad_id = item.find(conf.AD_ID_KEY).text
        output_dir = "%s/%s" % (img_dir, ad_id)
        img_sources = [img.find("src").text for
                       img in item.find(conf.IMGS_KEY).findall("value")]
        if img_sources and not os.path.exists(output_dir):
            os.makedirs(output_dir, 0755)
        for src in img_sources:
            filename = ntpath.basename(src)
            outpath = "%s/%s" % (output_dir, filename)
            if not os.path.exists(outpath):
                downloader.download_img(src, outpath)
            else:
                print("Img file already exists: %s (not overwriting)" % outpath)
        
        
if __name__=="__main__":

    # Handle command-line arguments
    (opts, args) = parser.parse_args()
    if not opts.input_file:
        parser.error("Input file required")

    # Download images
    download(opts.input_file, opts.img_dir)
