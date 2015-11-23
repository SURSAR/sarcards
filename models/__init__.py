# -*- coding: utf-8 -*-
"""
Models
======

`SQLAlchemy <http://www.sqlalchemy.org/>`_ based

Each item starts with +1VM. For each Item the Product_Provides - Product_Requires must be >= 0 (requires consumed first to allow require then provide)
source_item_id (onyl valid with specific product id) allows you to pull in the 'provides' of another Item into the current item (one way though you will often need one back too).
Templates can simply be existing item

.. graphviz:: graph.dot

.. automodule:: models.continuum

.. automodule:: models.user

.. automodule:: models.quote

.. automodule:: models.project

.. automodule:: models.product

.. automodule:: models.op

"""
from __future__ import division, absolute_import, print_function, unicode_literals

from sqlalchemy_continuum import make_versioned
from models.continuum import ContinuumPlugin

make_versioned(
    options={'native_versioning': True},
    plugins=[ContinuumPlugin()]
)
