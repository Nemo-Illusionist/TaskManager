from uuid import uuid4
from Services.SessionManager import RegistrationSession
from Services.dbManager import *
from hashlib import sha512
from typing import List


class User:
    Id: int
    Login: str

    def __init__(self, a=None):
        self.Id = a.Id
        self.Login = a.Login


def getHash(salt, password):
    return sha512((salt + password).encode('utf-8')).hexdigest()


def Authorization(Login, Pass):
    user = getUser(Login)
    if user is None:
        return None
    if getHash(user.Salt, Pass) == user.PassHash:
        return RegistrationSession(user.Id)
    return None


def Registration(Login, Pass, email, phone, name) -> bool:
    salt = sha512(str(uuid4()).encode('utf-8')).hexdigest()
    passHash = hash(salt, Pass)
    try:
        addUser(Login, passHash, salt, email, phone, name)
    except CommitException:
        return True
    return False


def GetUserInfo(Login) -> [UserInfoEntity, List[UserUrlEntity]]:
    user = getUser(Login)
    if user is None:
        return None
    return getUserInfo(user.Id), getUserUrl(user.Id)


def GetAllUser() -> List[User]:
    return [User(a) for a in getAllUser()]
