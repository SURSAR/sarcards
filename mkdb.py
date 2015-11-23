#! ./bin/python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import division, absolute_import, print_function, unicode_literals

import sqlalchemy as sa

#pylint: disable=unused-import
from web import db
import models
from models import member

sa.orm.configure_mappers()

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
