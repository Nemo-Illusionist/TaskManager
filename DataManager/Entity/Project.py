from pony.orm import *
from DataManager.dbManager import db


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