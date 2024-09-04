#!/usr/bin/env python3
"""Auth module"""
from typing import List, TypeVar
from flask import request


class Auth():
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a resource requires authentication to access"""
        if path and excluded_paths:
            if not path.strip().endswith('/'):
                path = path + '/'

            for p in excluded_paths:
                p = p.strip()

                if p.endswith('*') and path.startswith(p[:-1]):
                    return False

                if not p.endswith('/'):
                    p = p + '/'

                if p == path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """get value of authorization header"""
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """to be overloaded to retrieve the user instance for a request"""
        return None
