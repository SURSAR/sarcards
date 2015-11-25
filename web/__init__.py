# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

import sys
import os
import datetime
import json
from flask import Flask, render_template, render_template_string, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__, static_folder='../static', static_path='/static')

#app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['MAIL_DEFAULT_SENDER'] = 'Surrey <members@ssursar.org.uk>'
#app.config['PROPAGATE_EXCEPTIONS'] = True
#app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '123456790'

db = SQLAlchemy(app)

admin = Admin(app, name='SAR', url='/')
