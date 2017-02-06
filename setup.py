import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "good_ovening",
    version = "0.0.3",
    author = "Matthew Pierce",
    author_email = "piercemattd@gmail.com",
    description = (""" A web-crawler for extracting oven types and locations from
    listings at http://m.finn.no """),
    license = "BSD",
    keywords = "web-crawler oven Norway",
    url = "http://packages.python.org/good_ovening",
    packages=['good_ovening', 'good_ovening.db', 'good_ovening.fireplace_crawler',
              'good_ovening.fireplace_crawler.spiders'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Web Crawler",
        "License :: OSI Approved :: BSD License",
    ],
)
