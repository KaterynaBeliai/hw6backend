import secrets

SESSIONS = {}


class SessionStore:
    def create_session(self, data):
        sid = secrets.token_hex(16)
        SESSIONS[sid] = data
        return sid

    def get_session(self, session_id):
        if not session_id:
            return None
        return SESSIONS.get(session_id)

    def delete_session(self, session_id):
        if not session_id:
            return
        SESSIONS.pop(session_id, None)


sessions = SessionStore()


def create_session(data):
    return sessions.create_session(data)


def get_session(session_id):
    return sessions.get_session(session_id)


def delete_session(session_id):
    sessions.delete_session(session_id)
