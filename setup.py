#! bin/python
# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

from setuptools import setup

setup(
    name="sarcards",
    version="0.0.1",
    description="DB for SAR",
    author="Barnaby",
    author_email="b@Zi.iS",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Customer Service",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3"
    ],
    scripts=[
    ],
    packages=[
        "models",
        "web",
    ],
    package_data={
        'web': ['templates/*']
    },
    install_requires=[
        "Flask==0.10.1",
        "Flask-Mail==0.9.1",
        "Flask-SQLAlchemy==2.0",
        "mysqlclient==1.3.7",
        "SQLAlchemy-Continuum==1.1.5",
        "SQLAlchemy_Utils==0.30.11",
        "python-dateutil==2.4.2",
        "mock==1.0.1",
        "uwsgidecorators==1.1.0",
        "html2text==2015.6.21",
        "requests==2.7.0",
    ],
    extras_require={
        'dev': [
            "Sphinx",
            "sphinxcontrib-httpdomain",
            "pylint",
            "sphinxcontrib-autoanysrc",
            "alembic",
            "PyYAML",
            "pygraphviz==1.3rc2",
            "ERAlchemy",
            "coverage",
        ]
    }
)
