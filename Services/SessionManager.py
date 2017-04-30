from uuid import uuid4
from Services.dbManager import addSession


def RegistrationSession(userId):
    uuid = uuid4()
    addSession(uuid, userId)
    return uuid