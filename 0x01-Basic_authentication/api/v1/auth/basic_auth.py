#!/usr/bin/env python3
"""BasicAuth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """extracts base64-encoded username:password combo from auth header"""
        if authorization_header and isinstance(authorization_header, str):
            if authorization_header.startswith('Basic '):
                encoded_uname_pwd = authorization_header.split('Basic ', 1)[1]
                return encoded_uname_pwd
        return None
