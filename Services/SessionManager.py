from uuid import uuid4
from Services.dbManager import addSession, getSessions


def RegistrationSession(userId):
    struuid = str(uuid4())
    addSession(struuid, userId)
    return struuid


def ValidationSession(sessionId):
    session = getSessions(sessionId)
    if session is None:
        return None
    return session.UserId
