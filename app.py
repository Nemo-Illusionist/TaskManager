from flask import Flask, render_template, request, jsonify, escape, redirect, abort, url_for, make_response
from pony.orm import *
from pytz import timezone
from datetime import datetime
from hashlib import sha512
from uuid import uuid4
from urllib.parse import quote

app = Flask(__name__)
app.debug = True

db = Database()


class User(db.Entity):
    _table_ = "User"
    Id = PrimaryKey(int, auto=True)
    Login = Required(str, unique=True)
    PassHash = Required(str)
    salt = Required(str)


class UserInfo(db.Entity):
    _table_ = "UserInfo"
    Id = PrimaryKey(int, auto=True, unique=True)
    UserId = set(int, table='User', column='Id')
    Email = Optional(str)
    Phone = Optional(str)
    Name = Optional(str)


class UserUrl(db.Entity):
    _table_ = "UserUrl"
    Id = PrimaryKey(int, auto=True, unique=True)
    UserId = set(int, table='User', column='Id')
    Url = Required(str)


class Project(db.Entity):
    _table_ = "Project"
    Id = PrimaryKey(int, auto=True, unique=True)
    UserId = set(int, table='User', column='Id')
    ProjectName = Required(str)
    Status = Required(str)
    URL = Required(str)
    StartData = Required(str)
    EndData = Optional(str)
    ExpectedDate = Optional(str)


class ParticipantsProject(db.Entity):
    _table_ = "ParticipantsProject"
    Id = PrimaryKey(int, auto=True, unique=True)
    UserId = set(int, table='User', column='Id')
    ProjectId = set(int, table='Project', column='Id')


class ProjectInfo(db.Entity):
    _table_ = "ProjectInfo"
    Id = PrimaryKey(int, auto=True, unique=True)
    ProjectId = set(int, table='Project', column='Id')
    Text = Required(str)


class Task(db.Entity):
    _table_ = "Task"
    Id = PrimaryKey(int, auto=True, unique=True)
    ProjectId = set(int, table='Project', column='Id')
    UserId = set(int, table='User', column='Id')
    TaskName = Required(str)
    Comment = Optional(str)
    Priority = Required(int)
    Status = Required(str)
    StartData = Required(str)
    EndData = Optional(str)
    ExpectedDate = Optional(str)

