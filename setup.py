import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='qwer',
    version='0.1',
    description='Image dithering in python',

    author='Justas Trimailovas',
    author_email='j.trimailovas@gmail.com',

    url='https://github.com/trimailov/qwer',
    keywords=['image dithering'],

    long_description=read('README.rst'),

    entry_points='''
        [console_scripts]
        qwer=main:main
    ''',
)
