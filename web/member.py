# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

import os
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from jinja2 import Markup

from . import admin, db
from models.member import *

class MemberView(ModelView):
    """"""
    def _list_thumbnail(self, context, model, name):
        """"""
        if not model.image:
            return ''
        return Markup('<img src="%s">' % url_for(
            'static',
            filename=form.thumbgen_filename(model.image)
        ))
    column_formatters = {
        'image': _list_thumbnail
    }
    form_extra_fields = {
        'image': form.ImageUploadField(
            'Mugshot',
            base_path='static',
            thumbnail_size=(100, 100, True)
        )
    }

class TeamView(ModelView):
    """"""
    def _list_thumbnail(self, context, model, name):
        """"""
        if not model.logo:
            return ''
        return Markup('<img src="%s">' % url_for(
            'static',
            filename=form.thumbgen_filename(model.logo)
        ))
    column_formatters = {
        'logo': _list_thumbnail
    }
    form_extra_fields = {
        'logo': form.ImageUploadField(
            'Logo',
            base_path='static',
            thumbnail_size=(100, 100, True)
        )
    }

admin.add_view(ModelView(GlobalQualification, db.session))
admin.add_view(ModelView(GlobalRole, db.session))
admin.add_view(TeamView(Team, db.session))
admin.add_view(ModelView(TeamQualification, db.session))
admin.add_view(ModelView(TeamRole, db.session))

admin.add_view(MemberView(Member, db.session))
