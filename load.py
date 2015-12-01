#! bin/python

import sys
import csv
import fileinput
from models.member import *
from web import db

def main(files):
    roles = {}
    quals = {}
    status = {}

    team = Team(
        name='Surrey Search & Rescue'
    )
    db.session.add(team)
    for qual in "ST,tTl,TL,SP,SO,SM,DH2,DH3,DHGS,RP,RPS,RPC,Mod1,Mod2,Mod3,Mod4,Mod5,Mod6,RYA PB Lvl2,LRFR,Doctor,Nurse,Paramedic,4x4,Driver,Cat C1,NPPVL3".split(','):
        if qual in "tTl,RP,RPS,RPC".split(','):
            #local
            qual_obj = None
        else:
            #global
            qual_obj = GlobalQualification(
                title=qual
            )
            db.session.add(qual_obj)
        quals[qual] = TeamQualification(
            title=qual,
            team=team,
            global_qualification=qual_obj
        )
        db.session.add(quals[qual])

    for role in "Wading Team Leader,Flood Boat Operator,Water Incident Manager,Water Team Leader,Search Boat Operator,Level 2 (Hasty Search) Dog Handler,Level 3 (Area Search) Dog Handler,Ground Scenting Dog Handler,Search Technician,Trainee Team Leader,Team Leader,Search Planner,Search Operations,Search Manager,Medic,Doctor,Nurse,Paramedic,RPAS Pilot,RPAS Spotter,RPAS Controller".split(','):
        if role in "Search Technician,Team Leader,Search Planner,Search Operations,Search Manager,Medic,Doctor,Nurse,Paramedic".split(','):
            role_obj = GlobalRole(
                title=role
            )
            db.session.add(role_obj)
        else:
            role_obj = None
        roles[role] = TeamRole(
            title=role,
            team=team,
            global_role=role_obj
        )
        db.session.add(roles[role])

    status['Operational'] = Status(
        title="Operational"
    )
    db.session.add(status['Operational'])
    status['Non-Operational'] = Status(
        title="Non-Operational"
    )
    db.session.add(status['Non-Operational'])

    for row in csv.DictReader(fileinput.input(files)):
        member = Member(
            name=row['First Name'] + ' ' + row['Surname'],
            callsign=row['Callsign'],
            primary_role=row['Primary Title'],
            status=status[row['Status']],
            team=team,
            joined=datetime.datetime.strptime(row['Member Since'], "%d %b %Y")
        )
        for qual in "ST,tTl,TL,SP,SO,SM,DH2,DH3,DHGS,RP,RPS,RPC,Mod1,Mod2,Mod3,Mod4,Mod5,Mod6,RYA PB Lvl2,LRFR,Doctor,Nurse,Paramedic,4x4,Driver,Cat C1,NPPVL3".split(','):
            if row[qual] == "y":
                member.qualifications.append(quals[qual])
        for role in "Wading Team Leader,Flood Boat Operator,Water Incident Manager,Water Team Leader,Search Boat Operator,Level 2 (Hasty Search) Dog Handler,Level 3 (Area Search) Dog Handler,Ground Scenting Dog Handler,Search Technician,Trainee Team Leader,Team Leader,Search Planner,Search Operations,Search Manager,Medic,Doctor,Nurse,Paramedic,RPAS Pilot,RPAS Spotter,RPAS Controller".split(','):
            if row[role] == role:
                member.roles.append(roles[role])
        db.session.add(member)
    db.session.commit()

if __name__ == "__main__":
    main(sys.argv[1:])

