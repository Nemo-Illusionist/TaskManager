from pony.orm import *
from datetime import datetime

db = Database()


# region Entity
class ParticipantsProject(db.Entity):
    _table_ = "ParticipantsProject"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int)
    ProjectId = Required(int)


class Project(db.Entity):
    _table_ = "Project"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int)
    ProjectName = Required(str)
    Status = Required(str, default="Новый")
    URL = Required(str)
    StartData = Required(datetime)
    EndData = Optional(datetime)
    ExpectedDate = Optional(datetime)


class ProjectInfo(db.Entity):
    _table_ = "ProjectInfo"
    Id = PrimaryKey(int, auto=True)
    ProjectId = Required(int, unique=True)
    Text = Required(str)


class Task(db.Entity):
    _table_ = "Task"
    Id = PrimaryKey(int, auto=True)
    ProjectId = Required(int)
    UserId = Required(int)
    TaskName = Required(str)
    Comment = Optional(str)
    Priority = Required(int)
    Status = Required(str, default="Новый")
    StartData = Required(datetime)
    EndData = Optional(datetime)
    ExpectedDate = Optional(datetime)


class User(db.Entity):
    _table_ = "User"
    Id = PrimaryKey(int, auto=True)
    Login = Required(str, unique=True)
    PassHash = Required(str)
    Salt = Required(str)


class UserInfo(db.Entity):
    _table_ = "UserInfo"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int, unique=True)
    Email = Optional(str)
    Phone = Optional(str)
    Name = Optional(str)


class UserUrl(db.Entity):
    _table_ = "UserUrl"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int)
    Comment = Required(str)
    Url = Required(str)


# endregion

db.bind('sqlite', 'TaskManager.db', create_db=True)
db.generate_mapping(create_tables=True)


# region UserDB
@db_session
def addUser(login, pass_hash, salt, email, phone, name):
    User(Login=login, PassHash=pass_hash, Salt=salt)
    commit()
    id = select(r for r in User if r.Login == login).first().Id
    UserInfo(UserId=id, Email=email, Phone=phone, Name=name)
    commit()


@db_session
def addUserUrl(id, comment, url):
    UserUrl(UserId=id, Comment=comment, Url=url)
    commit()


@db_session
def getAllUser():
    return User.get()


@db_session
def getUser(login):
    return select(r for r in User if r.Login == login).first()


@db_session
def getUserInfo(id):
    return select(r for r in UserInfo if r.UserId == id).first()


@db_session
def getUserUrl(id):
    return select(r for r in UserInfo if r.UserId == id).get()


@db_session
def deleteUserUrl(id):
    delete(r for r in UserUrl if r.Id == id)
    commit()


# endregion


# region ProjectDB
@db_session
def addProject(userId, name, url, status, expected):
    p = Project(UserId=userId, ProjectName=name, URL=url)
    if status is not None:
        p.Status = status
    if expected is not None:
        p.ExpectedDate = expected
    commit()
    id = p.Id
    ParticipantsProject(UserId=userId, ProjectId=id)
    commit()

# endregion
