#!/usr/bin/env python3
"""SessionExpAuth module"""
from datetime import datetime, timedelta
from os import getenv
from typing import Optional
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessonExpAuth class"""
    def __init__(self):
        """Initialize a SessionExpAuth"""
        sesh_duration = getenv('SESSION_DURATION')
        try:
            sesh_duration = int(sesh_duration)
        # if sesh_duration is None or cannot cast to int
        except (TypeError, ValueError):
            sesh_duration = 0

        self.session_duration = sesh_duration

    def create_session(self, user_id=None) -> Optional[str]:
        """create a user session based on their id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None) -> Optional[str]:
        """returns a user id linked to a session based on an expiration"""
        if not session_id:
            return

        sesh_dict = self.user_id_by_session_id.get(session_id, None)
        if not sesh_dict:
            return

        user_id = sesh_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id

        created_at = sesh_dict.get('created_at')
        if not created_at:
            return

        sesh_end = created_at + timedelta(seconds=self.session_duration)
        current_time = datetime.now()

        if sesh_end < current_time:
            return
        return user_id
