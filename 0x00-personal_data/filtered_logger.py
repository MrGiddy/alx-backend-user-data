#!/usr/bin/env python3
"""Handling backend user data"""
import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Instantiate a RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """reduct values in incoming log record(s)"""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
