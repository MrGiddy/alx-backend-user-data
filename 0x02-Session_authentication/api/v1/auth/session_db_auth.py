#!/usr/bin/env python3
"""SessionDBAuth module"""
from datetime import datetime, timedelta
from typing import Optional
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None) -> Optional[str]:
        """creates and stores a new UserSession"""
        session_id = super().create_session(user_id)
        if not session_id:
            return
        sesh_data = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_sesh = UserSession(**sesh_data)
        user_sesh.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> Optional[str]:
        """returns user_id from a UserSession in db based on session_id"""
        try:
            user_sesh = UserSession().search({'session_id': session_id})
        except Exception:
            return

        if len(user_sesh) <= 0:
            return

        duration = timedelta(seconds=self.session_duration)
        sesh_exp_time = user_sesh[0].created_at + duration
        current_time = datetime.now()

        if sesh_exp_time < current_time:
            return
        return user_sesh[0].user_id

    def destroy_session(self, request=None):
        """destroys a UserSession in db based on session_id"""
        session_id = self.session_cookie(request)
        try:
            user_sesh = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if len(user_sesh) <= 0:
            return False

        user_sesh[0].remove()
        return True
