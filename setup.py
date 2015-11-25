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
        "Flask-Admin==1.2.0",
        "Flask-SQLAlchemy==2.0",
        "mysqlclient==1.3.7",
    ],
    extras_require={
        'dev': [
            "pylint",
            "Flask-DebugToolbar",
        ]
    }
)
