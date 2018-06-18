# encoding: utf-8

import re
import unittest

EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class EmailValidation:
    def __init__(self, email_to_validate):
        if EMAIL_PATTERN.match(email_to_validate) is None:
            raise ValueError('Invalid email')
        else:
            self.email = email_to_validate

    def __str__(self):
        return self.email


class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)

        self.first_name = first_name
        self.last_name = last_name
        self.email = EmailValidation(email)
