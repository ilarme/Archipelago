import sys

from sqlalchemy.dialects.postgresql import JSON
from db import DB
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import openpyxl as opx
from sqlalchemy import insert
import sqlalchemy as sql
from sqlalchemy.orm import declarative_base

db = DB(sys.argv[1])
conn = db.conn

wb = opx.load_workbook("input.xlsx")
sa = wb.active

Base = declarative_base()



class Teams(Base):
    __tablename__ = 'teams_1'
    id = Column(Integer, primary_key=True)
    context_id = Column(Integer)
    team_name = Column(String)
    head_id = Column(String)
    team_id = Column(Integer)
    additional_data = Column(JSON)


class Projects(Base):
    __tablename__ = 'projects_1'
    id = Column(Integer, primary_key=True)
    context_id = Column(Integer)
    name = Column(String)
    link = Column(String)
    project_id = Column(Integer)
    agenda = Column(String)
    track_id = Column(Integer)
    additional_data = Column(JSON)


class TeamsProjects(Base):
    __tablename__ = 'teams_projects_1'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    project_id = Column(Integer)


def test_decorator(function):
    def new_function():
        print("function was changed")
        function()

    return new_function


@test_decorator
def test_function():
    print("test function")


def InsertTeam(context_id, team_name, head_id, team_id, additional_data):
    try:
        res = conn.execute(
            insert(Teams),
            [
                {"context_id": context_id, "team_name": team_name, "head_id": head_id, "team_id": team_id,
                 "additional_data": additional_data}
            ]
        )
        conn.commit()
    except Exception as e:
        print('error while inserting team == ', str(e))


def InsertProject(context_id, name, link, project_id, agenda, track_id, additional_data):
    try:
        res = conn.execute(
            insert(Projects),
            [
                {"context_id": context_id, "name": name, "link": link, "project_id": project_id, "agenda": agenda,
                 "track_id": track_id, "additional_data": additional_data}
            ]
        )
        conn.commit()
    except Exception as e:
        print('error while inserting project == ', str(e))


def InsertTeamsProjects(team_id, project_id):
    try:
        res = conn.execute(
            insert(TeamsProjects),
            [
                {"team_id": team_id, "project_id": project_id}
            ]
        )
        conn.commit()
    except Exception as e:
        print('error while inserting teams projects == ', str(e))


def LoadAll():
    for row in range(2, sa.max_row + 1):
        context_id = 32
        name = sa['C' + str(row)].value
        link = sa['I' + str(row)].value
        project_id = None
        agenda = sa['H' + str(row)].value
        track_id = None
        additional_data = ""
        InsertProject(context_id, name, link, project_id, agenda, track_id, additional_data)


if __name__ == "main":
    Session = sessionmaker(bind=db.engine)
    session = Session()
    LoadAll()
