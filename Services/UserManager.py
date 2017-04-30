from Services.SessionManager import RegistrationSession
from Services.dbManager import *
from hashlib import sha512


def getHash(salt, password):
    return sha512((salt + password).encode('utf-8')).hexdigest()


def Authorization(Login, Pass):
    user = getUser(Login)
    if user is None:
        return None
    if getHash(user.Salt, Pass) == user.PassHash:
        return RegistrationSession(user.Id)
    return None


def Registration(Login, Pass, email, phone, name):
    salt = sha512(str(uuid4()).encode('utf-8')).hexdigest()
    passHash = hash(salt, Pass)
    try:
        addUser(Login, passHash, salt, email, phone, name)
    except CommitException:
        return True
    return False
