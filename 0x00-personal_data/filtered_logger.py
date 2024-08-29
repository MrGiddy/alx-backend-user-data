#!/usr/bin/env python3
"""Handling backend user data"""
import logging
import re
from typing import List
import mysql.connector
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a MySQL db connection """
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        database=database,
        password=password
    )
    return conn


def main() -> None:
    """displays filtered/redacted user data"""
    # obtain a database connection using get_db
    connection = get_db()
    with connection.cursor() as cursor:
        # retrieve all cols names and rows in the users table
        query = 'SELECT * FROM users;'
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = cursor.column_names
        # display each row with PII obfuscated
        logger = get_logger()
        paired = []
        for row in rows:
            for k, v in zip(columns, row):
                paired.append(f'{k}={v}')
            message = ';'.join(paired) + ';'
            logger.info(message)


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


if __name__ == '__main__':
    main()
