# -*- coding: utf-8 -*-
"""
JSON Api
========

WWW
^^^

.. autoflask:: web.uwsgi:app
   :undoc-static:

>>> from web import *
>>> import datetime
>>> json = CustomJSONEncoder()
>>> json.default(datetime.datetime(2011,2,11,20,0,0,0))
'2011-02-11T20:00:00'
>>> json.default(datetime.date(2000,2,29))
'2000-02-29'
>>> json.default(None)
Traceback (most recent call last):
TypeError:
>>> from models.user import User
>>> user = User()
>>> user.username = 'no@example.com'
>>> with app.test_request_context('/'):
...     with MAIL.record_messages() as outbox:
...         mail([user], 'test', {})
...         assert outbox[0].subject == 'test'
...         outbox[0].body
'# test\\n\\nfoobar\\n\\n'
"""
from __future__ import division, absolute_import, print_function, unicode_literals

#pylint: disable=unused-import
import sys
try:
    import uwsgi
except ImportError:
    from mock import MagicMock
    sys.modules['uwsgi'] = MagicMock()
    sys.modules['uwsgidecorators'] = MagicMock()

import os
import datetime
import json
from flask import Flask, render_template, render_template_string
from flask.json import JSONEncoder
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import html2text

app = Flask(__name__)

app.config['TESTING'] = os.environ.get('TESTING', False)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['MAIL_DEFAULT_SENDER'] = 'Wirehive Quote Tool <support@wirehive.net>'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class CustomJSONEncoder(JSONEncoder):
    """"""
    #pylint: disable=method-hidden
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return JSONEncoder.default(self, obj)
app.json_encoder = CustomJSONEncoder

MAIL = Mail(app)

def mail(recipients, template, data, bcc=None):
    """Send email"""
    first = True
    for recipient in recipients:
        body = render_template(
            template + '.body',
            now=datetime.datetime.now(),
            to=recipient,
            **data
        )
        subject = render_template(
            template + '.subject',
            now=datetime.datetime.now(),
            to=recipient,
            **data
        )
        MAIL.send(
            Message(
                recipients=["b@zi.is"], #TODO: recipient.username,
                extra_headers={
                    "X-BRS-TO": recipient.username,
                    "X-BRS-BCC": ",".join([bccuser.username for bccuser in bcc]) if first and bcc else ""
                },
                #TODO: bcc=bcc,
                subject=subject,
                html=body,
                body=mail.makeplain.handle(body)
            )
        )
        first = False

mail.makeplain = html2text.HTML2Text()
mail.makeplain.unicode_snob = True
mail.makeplain.ul_item_mark = '⚫'
mail.makeplain.ignore_images = True

