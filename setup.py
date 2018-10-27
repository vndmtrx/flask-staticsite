import os
import re
import sys

from setuptools import setup, find_packages

DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

README = open(rel('README.md')).read()
INIT_PY = open(rel('flask_staticsite', '__init__.py')).read()
VERSION = re.search("__version__ = '([^']+)'", INIT_PY).group(1)

setup(
    name='Flask-StaticSite',
    version=VERSION,
    url='https://github.com/vndmtrx/Flask-StaticSite',
    license='Apache',
    author='Eduardo Rolim',
    author_email='vndmtrx@gmail.com',
    description='Provides static pages to a Flask application.',
    long_description=README,
    packages=find_packages(exclude=["tests", "examples"]),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=1.0.2',
        'PyYAML>=3.13',
        'six>=1.11.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities',
        'Framework :: Flask',
    ]
)
