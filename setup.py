import os
import re
import sys

from setuptools import setup

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
    packages=[
        'flask_staticsite'
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'PyYAML>=3.10'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
