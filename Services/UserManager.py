from Services.dbManager import *
from hashlib import sha512


def getHash(salt, password):
    return sha512((salt + password).encode('utf-8')).hexdigest()


def RegistrationSession(userId):
    id = uuid4()
    addSession(id, userId)
    return id


def Authorization(Login, Pass):
    user = getUser(Login)
    if user is None:
        return None
    if getHash(user.Salt, Pass) == user.PassHash:
        return RegistrationSession(user.Id)
    return None


def Registration(Login, Pass):
    salt = sha512(str(uuid4()).encode('utf-8')).hexdigest()
    passHash = hash(salt, Pass)
    try:
        addUser(Login, passHash, salt)
    except CommitException:
        return None
    userId = getUser(Login).Id
    return RegistrationSession(userId)
