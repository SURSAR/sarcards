# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

import subprocess
import uuid
import datetime
import base64
import struct
from flask import url_for, render_template_string
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from flask_admin.actions import action
from jinja2 import Markup
from PyPDF2 import PdfFileReader, PdfFileWriter
from weasyprint import HTML

from . import admin, db
from models.member import * #pylint: disable=wildcard-import, unused-wildcard-import

class MemberView(ModelView):
    """"""
    def after_model_change(self, frm, model, is_created):
        """"""
        if model.image:
            subprocess.call([
                "/usr/local/bin/convert",
                "static/%s[0]" % model.image,
                "-alpha",
                "off",
                "-strip",
                "-colorspace",
                "gray",
                "-normalize",
                "-gamma",
                "2.2",
                "-quality",
                "100",
                "jpg:/tmp/cv.jpg"
            ])
            face = subprocess.check_output([
                "./face.py",
                "/tmp/cv.jpg"
            ]).decode('ascii')[:-1]
            subprocess.call([
                "/usr/local/bin/convert",
                "static/%s[0]" % model.image,
                "-alpha",
                "off",
                "-strip",
                "-crop",
                face,
                "+repage",
                "-colorspace",
                "gray",
                "-resize",
                "70x70",
                "-normalize",
                "-gamma",
                "2.2",
                "-define",
                "jpeg:extent=1024",
                "-quality",
                "100",
                "jpg:static/thumb_%s" % model.image,
            ])

    def _list_thumbnail(self, context, model, name):
        """"""
        if not model.image:
            return ''
        return Markup('<img src="%s">' % url_for(
            'static',
            filename="thumb_" + model.image
        ))
    column_formatters = {
        'image': _list_thumbnail
    }
    form_extra_fields = {
        'image': form.FileUploadField(
            'Mugshot',
            base_path='static',
            namegen=lambda x, y: str(uuid.uuid4()),
            allow_overwrite=False
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
        'logo': form.FileUploadField(
            'Logo',
            base_path='static',
            namegen=lambda x, y: str(uuid.uuid4()),
            allow_overwrite=False
        )
    }

class IssueView(ModelView):
    """"""
    @action('issue', 'Issue', 'Are you sure you want to issue selected cards?')
    def action_issue(self, ids):
        """"""
        for issue in Issue.query.filter(Issue.id.in_(ids)):
            if issue.issued != None:
                raise Exception("Already Issued")
            issue.issued = datetime.datetime.now()
            item = issue.subject
            photo = open('static/thumb_' + item.image, 'rb').read()
            data = """
FN:%s
ORG:%s
TITLE:%s
ANNIVERSARY:%s
X-EXPIRY:%s
NOTE:roles=%s\\nqualifications=%s\\ncallsign=%s\\nstatus=%s
""" % (
    item.name,
    item.team.name,
    item.primary_role,
    "%d%d%d" % (item.joined.year, item.joined.month, item.joined.day),
    "%d%d%d" % (item.joined.year + 10, item.joined.month, item.joined.day),
    ",".join([role.title for role in item.roles]),
    ",".join([qual.title for qual in item.qualifications]),
    item.callsign,
    item.status.title
)
            data += "REV:%d%d%d\n" % (issue.issued.year, issue.issued.month, issue.issued.day)
            data = data.replace("\n", "\r\n")

            bdata = (
                b"BEGIN:VCARD\r\nVERSION:3.0" +
                data.encode('utf-8') +
                b"PHOTO;JPEG;ENCODING=BASE64:" + base64.b64encode(photo) +
                b"\r\nEND:VCARD\r\n\r\n"
            )
            with open("static/" + item.image + ".ndef", "wb") as out:
                out.write(b"\xC2\x0A")
                out.write(struct.pack(">i", len(bdata)))
                out.write(b"text/vcard" + bdata)
            subprocess.call([
                "gpg",
                "-z",
                "9",
                "-u",
                "252E0A0E",
                "-b",
                "static/" + item.image + ".ndef"
            ])
        charity_number
        HTML(
        	render_template_string("test.html.j2", {
            	"surname": item.name.split()[-1],
            	"given": " ".join(item.name.split()[:-1]),
            	"role": item.primary_role,
            	"joined": item.joined,
            	"issued": issue.issued,
            	"expiry": issue.issued + date(issue.issued.year + 10, 1, 1) - date(issue.issued.year, 1, 1),
            	"charity": item.team.charity_number
        	})
		).write_pdf('/tmp/sarcard.pdf')

		output = PdfFileWriter()
		pdfOne = PdfFileReader(open("../blank.pdf", "rb"))
		pdfTwo = PdfFileReader(open("/tmp/sarcard.pdf", "rb"))
		output.addPage(pdfOne.getPage(0))
		output.getPage(0).mergePage(pdfTwo.getPage(0))
		outputStream = open("static/" + item.image + ".pdf", "wb")
		output.write(outputStream)
		outputStream.close()
        db.session.commit()

admin.add_view(ModelView(GlobalQualification, db.session))
admin.add_view(ModelView(GlobalRole, db.session))
admin.add_view(TeamView(Team, db.session))
admin.add_view(ModelView(TeamQualification, db.session))
admin.add_view(ModelView(TeamRole, db.session))
admin.add_view(ModelView(Status, db.session))
admin.add_view(MemberView(Member, db.session))

admin.add_view(ModelView(IssueReason, db.session))
admin.add_view(IssueView(Issue, db.session))
