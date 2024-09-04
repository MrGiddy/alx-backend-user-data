#!/usr/bin/env python3
"""BasicAuth module"""
import base64
import binascii
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """extracts base64-encoded username:password combo from auth header"""
        if authorization_header and isinstance(authorization_header, str):
            if authorization_header.startswith('Basic '):
                return authorization_header.split('Basic ', 1)[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """decodes a base64-encoded auth header value"""
        if isinstance(base64_authorization_header, str):
            try:
                byte_string = base64.b64decode(base64_authorization_header)
                return byte_string.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """returns user email and password from Base64-decoded value"""
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                if ':' in decoded_base64_authorization_header:
                    uname, pwd = decoded_base64_authorization_header.split(':')
                    return (uname, pwd)
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """returns a User based on their credentials (email and password)"""
        if user_email and user_pwd:
            if isinstance(user_email, str) and isinstance(user_pwd, str):
                users = User().search({'email': user_email})
                if len(users) <= 0:
                    return None
                if users[0].is_valid_password(user_pwd):
                    return users[0]
