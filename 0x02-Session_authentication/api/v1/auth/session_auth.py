#!/usr/bin/env python3
"""SessionAuth module"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user id"""
        if not user_id or not isinstance(user_id, str):
            return
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
