# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

from flask_admin.contrib.sqla import ModelView
from flask_admin import form

from . import admin, db
from models.member import Member

class MemberView(ModelView):
    form_extra_fields = {
        'path': form.ImageUploadField(
            'Image',
            base_path='/tmp',
            thumbnail_size=(100, 100, True)
        )
    }

admin.add_view(MemberView(Member, db.session))
