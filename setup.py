"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
#from codecs import open
#from os import path

setup(
    name='pyFS',
    version='0.1.0',
    description='Python API for FS2000.', 
    packages=find_packages(include=['Analysis', 'BatchController',
        'ModelDefinition', 'Output'])
)