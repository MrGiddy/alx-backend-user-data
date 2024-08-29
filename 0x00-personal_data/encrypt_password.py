#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password as a byte string"""
    # make the pwd a bytes object
    password = bytes(password, encoding='utf-8')
    # hash the pwd with a random salt
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    return password
