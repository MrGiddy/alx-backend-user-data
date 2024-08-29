#!/usr/bin/env python3
"""Handling backend user data"""
import re
from typing import List


def replace(
        field: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """redacts part(s) of a message"""
    pattern = f'{field}=[^{separator}]+'
    separator = f'{field}={redaction}'
    return re.sub(pattern, separator, message)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """returns an obfuscated log message"""
    for field in fields:
        message = replace(field, redaction, message, separator)
    return message
