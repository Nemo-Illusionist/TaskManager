from pony.orm import *

from DataManager.Entity import User

db = Database()

db.bind('sqlite', 'TaskManager.db', create_db=True)
db.generate_mapping(create_tables=True)


@db_session
def addUser(login, pass_hash, salt):
    User(Login=login, PassHash=pass_hash, Salt=salt)
    commit()


