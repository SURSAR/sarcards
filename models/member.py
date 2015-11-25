# -*- coding: utf-8 -*-
""""""
from __future__ import division, absolute_import, print_function, unicode_literals

from web import db

class GlobalQualification(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    def __str__(self):
        return self.title

class GlobalRole(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    def __str__(self):
        return self.title

class Team(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    charity_number = db.Column(db.String(255))
    address = db.Column(db.String(4000), nullable=False)
    def __str__(self):
        return self.name

class TeamQualification(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    team_id =  db.Column(db.Integer, db.ForeignKey(Team.id), nullable=False)
    team = db.relationship(Team, backref='qualifications')
    global_id = db.Column(db.Integer, db.ForeignKey(GlobalQualification.id))
    global_qualification = db.relationship(GlobalQualification, backref='team_qualifications')
    def __str__(self):
        return self.title

class TeamRole(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    team_id =  db.Column(db.Integer, db.ForeignKey(Team.id), nullable=False)
    team = db.relationship(Team, backref='roles')
    global_id = db.Column(db.Integer, db.ForeignKey(GlobalRole.id))
    global_role = db.relationship(GlobalRole, backref='team_roles')
    def __str__(self):
        return self.title

class Member(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    team_id = db.Column(db.Integer, db.ForeignKey(Team.id))
    team = db.relationship(Team, backref='members')
    qualifications = db.relationship(TeamQualification, secondary='member_team_qualification', backref='members')
    roles = db.relationship(TeamRole, secondary='member_team_role', backref='members')
    def __str__(self):
        return self.name

#pylint: disable=invalid-name
MemberTeamQualification = db.Table(
    'member_team_qualification',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('member_id',db.Integer, db.ForeignKey(Member.id)),
    db.Column('qualification_id',db.Integer, db.ForeignKey(TeamQualification.id)),
)

MemberTeamRole = db.Table(
    'member_team_role',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('member_id',db.Integer, db.ForeignKey(Member.id)),
    db.Column('role_id',db.Integer, db.ForeignKey(TeamRole.id)),
)
