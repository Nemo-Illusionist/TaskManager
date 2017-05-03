from typing import List
from pony.orm import *
from datetime import datetime

db = Database()


# region Entity
class ParticipantsProjectEntity(db.Entity):
    _table_ = "ParticipantsProject"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int)
    ProjectId = Required(int)


class ProjectEntity(db.Entity):
    _table_ = "Project"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int)
    ProjectName = Required(str)
    Text = Required(str)
    Status = Required(str, default="Новый")
    URL = Required(str)
    StartData = Required(datetime)
    ExpectedDate = Optional(datetime)


class TaskEntity(db.Entity):
    _table_ = "Task"
    Id = PrimaryKey(int, auto=True)
    ProjectId = Required(int)
    UserId = Required(int)
    TaskName = Required(str)
    Comment = Optional(str)
    Priority = Required(int)
    Status = Required(str, default="Новый")
    StartData = Required(datetime)
    ExpectedDate = Optional(datetime)


class UserEntity(db.Entity):
    _table_ = "User"
    Id = PrimaryKey(int, auto=True)
    Login = Required(str, unique=True)
    PassHash = Required(str)
    Salt = Required(str)


class UserInfoEntity(db.Entity):
    _table_ = "UserInfo"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int, unique=True)
    Email = Optional(str)
    Phone = Optional(str)
    Name = Optional(str)


class UserUrlEntity(db.Entity):
    _table_ = "UserUrl"
    Id = PrimaryKey(int, auto=True)
    UserId = Required(int)
    Comment = Required(str)
    Url = Required(str)


class SessionsEntity(db.Entity):
    _table_ = "Sessions"
    Id = PrimaryKey(str)
    UserId = Required(int)
    Active = Required(bool, default=True)


# endregion

db.bind('sqlite', 'TaskManager.db', create_db=True)
db.generate_mapping(create_tables=True)


# region UserDB
@db_session
def addUser(login, hashPass, salt, email, phone, name):
    UserEntity(Login=login, PassHash=hashPass, Salt=salt)
    commit()
    id = select(r for r in UserEntity if r.Login == login).first().Id
    UserInfoEntity(UserId=id, Email=email, Phone=phone, Name=name)
    commit()


@db_session
def addUserUrl(id, comment, url):
    UserUrlEntity(UserId=id, Comment=comment, Url=url)
    commit()


@db_session
def getAllUser() -> List[UserEntity]:
    return UserEntity.get()


@db_session
def getUser(login) -> UserEntity:
    return select(r for r in UserEntity if r.Login == login).first()


@db_session
def getUserInfo(id) -> UserInfoEntity:
    return select(r for r in UserInfoEntity if r.UserId == id).first()


@db_session
def getUserUrl(id) -> UserUrlEntity:
    return select(r for r in UserUrlEntity if r.UserId == id).get()


# endregion

# region Sessions
@db_session
def getSessions(sessionId) -> SessionsEntity:
    return select(r for r in SessionsEntity if r.Id == sessionId and r.Active).first()


@db_session
def addSession(sessionId, userId):
    SessionsEntity(Id=sessionId, UserId=userId)
    commit()


@db_session
def disabledSession(sessionId):
    s = select(r for r in SessionsEntity if r.Id == sessionId and r.Active).first()
    s.Active = False
    commit()


# endregion

# region ProjectDB
@db_session
def addProject(userId, name, url, status, expected, info):
    p = ProjectEntity(UserId=userId, ProjectName=name, URL=url,
                      StartData=datetime.now(), Text=info)
    if status is not None:
        p.Status = status
    if expected is not None:
        p.ExpectedDate = expected
    commit()
    ParticipantsProjectEntity(UserId=userId, ProjectId=p.Id)
    commit()


@db_session
def getProject(userId):
    ProjectsId = select(r for r in ParticipantsProjectEntity
                        if r.UserId == userId).get()
    return

# endregion
