#!/usr/bin/env python3
"""Auth module"""
from typing import List, TypeVar
from flask import request


class Auth():
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a resource requires authentication to access"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path = path + '/'

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """get value of authorization header"""
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method"""
        return None
