from pony.orm import *
from DataManager.dbManager import db

class ProjectInfo(db.Entity):
    _table_ = "ProjectInfo"
    Id = PrimaryKey(int, auto=True)
    ProjectId = Required(int, unique=True)
    Text = Required(str)
