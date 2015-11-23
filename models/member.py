# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

from web import db

class Member(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    def __str__(self):
        return self.title
