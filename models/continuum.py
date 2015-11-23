# -*- coding: utf-8 -*-
"""
Versioning
^^^^^^^^^^

`SQLAlchemy-Continuum <https://sqlalchemy-continuum.readthedocs.org/en/latest/>`_ to automatically version models.

.. doctest::
    :hide:

    >>> from models.continuum import *
    >>> import flask
    >>> app = flask.Flask('test')
    >>> with app.test_request_context('/', environ_base={'REMOTE_USER':'1'}):
    ...    c = ContinuumPlugin()
    ...    assert c.transaction_args(None, None) == {'remote_addr': None, 'user_id': 1}
"""
from __future__ import division, absolute_import, print_function, unicode_literals

from sqlalchemy_continuum.plugins.base import Plugin
from flask import request

def _fetch_current_user_id():
    """"""
    return int(request.environ.get('REMOTE_USER'))

def _fetch_remote_addr():
    """"""
    return request.remote_addr

class ContinuumPlugin(Plugin):
    """Tie transactions to our authentication"""
    def __init__(self, current_user_id_factory=None, remote_addr_factory=None):
        """"""
        self.current_user_id_factory = (
            _fetch_current_user_id if current_user_id_factory is None
            else current_user_id_factory
        )
        self.remote_addr_factory = (
            _fetch_remote_addr if remote_addr_factory is None
            else remote_addr_factory
        )

    def transaction_args(self, uow, session):
        """"""
        return {
            'user_id': self.current_user_id_factory(),
            'remote_addr': self.remote_addr_factory()
        }
