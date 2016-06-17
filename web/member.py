# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

import subprocess
import uuid
import datetime
import base64
import struct
from flask import url_for, render_template
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from flask_admin.actions import action
from jinja2 import Markup
from PyPDF2 import PdfFileReader, PdfFileWriter
from weasyprint import HTML
import datetime

from . import admin, db
from models.member import * #pylint: disable=wildcard-import, unused-wildcard-import

class MemberView(ModelView):
    """"""
    column_default_sort = ('id', True)
    column_searchable_list = ('name', 'primary_role', 'team.name', 'callsign', 'status.title')

    @action('test_pdf', 'Sample')
    def test_pdf(self, ids):

        for item in Member.query.filter(Member.id.in_(ids)):
            HTML(
                string=render_template(
                    "card.html.j2",
                    surname=item.name.split()[-1],
                    given=" ".join(item.name.split()[:-1]),
                    role=item.primary_role,
                    joined=item.joined.strftime("%d %b %Y"),
                    issued=datetime.datetime.now().date().strftime("%d %b %Y"),
                    expiry=datetime.datetime.now().date().strftime("%d %b %Y"),
                    charity=item.team.charity_number,
                    callsign=item.callsign,
                    status='sample', #item.status.title,
                    status_color='#D90000', # if item.status.title.startswith('Non') else '#4c8c2b',
                    image=item.image,
                    logo=item.team.logo
                )
            ).write_pdf('/tmp/sarcard.pdf')
            HTML(
                string=render_template(
                    "card_back.html.j2",
                    role="<br />".join([role.title for role in item.roles]),
                    qual="<br />".join([qual.title for qual in item.qualifications]),
                    team=item.team.name,
                    add=item.team.address
                )
            ).write_pdf('/tmp/sarcard2.pdf')
    
            output = PdfFileWriter()
            pdfOne = PdfFileReader("blank.pdf")
            pdfTwo = PdfFileReader("/tmp/sarcard.pdf")
            pdfThree = PdfFileReader("/tmp/sarcard2.pdf")
            output.addPage(pdfOne.getPage(0))
            output.getPage(0).mergePage(pdfTwo.getPage(0))
            output.addPage(pdfOne.getPage(1))
            output.getPage(1).mergePage(pdfThree.getPage(0))
            outputStream = open("static/sam_" + item.image + ".pdf", "wb")
            output.write(outputStream)
            outputStream.close()

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
            subprocess.call([
                "/usr/local/bin/convert",
                "static/%s[0]" % model.image,
                "-strip",
                "-resize",
                "300x400",
                "-compose",
                "src",
                "-gravity",
                "south",
                "-extent",
                "300x400",
                "png:static/hi_%s" % model.image,
            ])

    def _list_thumbnail(self, context, model, name):
        """"""
        if not model.image:
            return ''
        return Markup('<a href="%s"><img src="%s"></a>' % (
            url_for(
                'static',
                filename="sam_" + model.image + ".pdf"
            ),
            url_for(
                'static',
                filename="thumb_" + model.image
            )
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
            filename="thumb_" + model.logo
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

    def after_model_change(self, frm, model, is_created):
        """"""
        if model.logo:
            subprocess.call([
                "/usr/local/bin/convert",
                "static/%s[0]" % model.logo,
                "-alpha",
                "off",
                "-strip",
                "-resize",
                "70x70",
                "-quality",
                "80",
                "jpg:static/thumb_%s" % model.logo,
            ])
            subprocess.call([
                "/usr/local/bin/convert",
                "static/%s[0]" % model.logo,
                "-strip",
                "-resize",
                "300x400",
                "-compose",
                "src",
                "-gravity",
                "south",
                "-extent",
                "300x400",
                "png:static/hi_%s" % model.logo,
            ])

class IssueView(ModelView):
    """"""

    column_default_sort = ('requested', True)
    column_list = ('subject', 'subject.callsign', 'requester', 'issuer', 'reason', 'requested', 'issued', 'reason')

    def _list_links(self, context, model, name):
        """"""
        if model.subject.image is None:
            return model.subject

        return Markup('%s <a href="%s">NDEF</a> <a href="%s">PDF</a>' % (
            model.subject,
            url_for(
                'static',
                filename=model.subject.callsign.replace('/','_') + ".ndef"
            ),
            url_for(
                'static',
                filename=model.subject.callsign.replace('/','_') + ".pdf"
            )
        ))

    column_formatters = {
        'subject': _list_links
    }


    @action('issue', 'Issue', 'Are you sure you want to issue selected cards?')
    def action_issue(self, ids):
        """"""
        for issue in Issue.query.filter(Issue.id.in_(ids)):
            if issue.issued != None:
                raise Exception("Already Issued")
            issue.issued = datetime.datetime.now()
            db.session.commit()
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
            with open("static/" + item.callsign.replace('/','_') + ".ndef", "wb") as out:
                out.write(b"\xC2\x0A")
                out.write(struct.pack(">i", len(bdata)))
                out.write(b"text/vcard" + bdata)
            
            #subprocess.call([
            #    "gpg",
            #    "-z",
            #    "9",
            #    "-u",
            #    "252E0A0E",
            #    "-b",
            #    "static/" + item.image + ".ndef"
            #])

            html = render_template(
                "card.html.j2",
                surname=item.name.split()[-1],
                given=" ".join(item.name.split()[:-1]),
                role=item.primary_role,
                joined=item.joined.strftime("%d %b %Y"),
                issued=issue.issued.strftime("%d %b %Y"),
                expiry=(issue.issued + (datetime.date(issue.issued.year + 10, 1, 1) - datetime.date(issue.issued.year, 1, 1))).strftime("%d %b %Y"),
                charity=item.team.charity_number,
                callsign=item.callsign,
                status=item.status.title,
                status_color='#D90000' if item.status.title.startswith('Non') else '#4c8c2b',
                image=item.image,
                logo=item.team.logo
            )

            print(html)

            HTML(
                string=html
            ).write_pdf('/tmp/sarcard.pdf')
            
            html = render_template(
                "card_back.html.j2",
                role="<br />".join([role.title for role in item.roles]),
                qual="<br />".join([qual.title for qual in item.qualifications]),
                team=item.team.name,
                add=item.team.address
            )

            print(html)

            HTML(
                string=html
            ).write_pdf('/tmp/sarcard2.pdf')
    
            output = PdfFileWriter()
            pdfOne = PdfFileReader("blank.pdf", strict = False)
            pdfTwo = PdfFileReader("/tmp/sarcard.pdf", strict = False)
            pdfThree = PdfFileReader("/tmp/sarcard2.pdf", strict = False)
            output.addPage(pdfOne.getPage(0))
            output.getPage(0).mergePage(pdfTwo.getPage(0))
            output.addPage(pdfOne.getPage(1))
            output.getPage(1).mergePage(pdfThree.getPage(0))
            outputStream = open("static/" + item.callsign.replace('/','_') + ".pdf", "wb")
            output.write(outputStream)
            outputStream.close()

admin.add_view(ModelView(GlobalQualification, db.session))
admin.add_view(ModelView(GlobalRole, db.session))
admin.add_view(TeamView(Team, db.session))
admin.add_view(ModelView(TeamQualification, db.session))
admin.add_view(ModelView(TeamRole, db.session))
admin.add_view(ModelView(Status, db.session))
admin.add_view(MemberView(Member, db.session))

admin.add_view(ModelView(IssueReason, db.session))
admin.add_view(IssueView(Issue, db.session))
