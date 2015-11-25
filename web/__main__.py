# -*- coding: utf-8 -*-
"""
"""
from __future__ import division, absolute_import, print_function, unicode_literals

from web.uwsgi import app #pylint: disable=wildcard-import,unused-wildcard-import
from flask_debugtoolbar import DebugToolbarExtension

app.debug = True

#toolbar = DebugToolbarExtension(app)

app.run()
