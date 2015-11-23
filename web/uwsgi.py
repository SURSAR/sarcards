# -*- coding: utf-8 -*-
"""
Flask App
^^^^^^^^^

Runs :doc:`www`

Python3 in VirtualEnv

Runs a SNMP server for engine and app metrics
"""
from __future__ import division, absolute_import, print_function, unicode_literals

import sqlalchemy as sa

#pylint: disable=unused-import
from . import app

sa.orm.configure_mappers()
