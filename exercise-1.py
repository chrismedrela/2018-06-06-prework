# encoding: utf-8

"""
Single Responsibility Principle to jedna z zasad SOLID. Mówi ona, że każda klasa
powinna mieć tylko jeden obszar odpowiedzialności i tylko jeden powód do zmiany.
Poniżej przedstawiono klasę Person, która reprezentuje pojedynczą osobę - jej
imię, nazwisko oraz adres mailowy. Jest to przykład złamania tej zasady,
ponieważ w środku niej znajduje się walidacja adresu email.
Jako ćwiczenie, spróbuj zrefaktoryzować ten kod tak, aby sama walidacja znalazła
się w osobnej klasie reprezentującej adres email.
"""

import re
import unittest
from unittest import TestCase


EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)

        self.first_name = first_name
        self.last_name = last_name
        self.email = EmailAddress(email)



class EmailAddress:
    def __init__(self, email):
        self.email = self.validate(email)

    def validate(self, email):
        assert isinstance(email, str)

        if EMAIL_PATTERN.match(email) is None:
            raise ValueError('Invalid email')
        else:
            return email


class EmailAddressTest(TestCase):
    def test_can_store_valid_address(self):
        valid_email = "jan.kowalski@gmail.com"

        email = EmailAddress(valid_email)

        self.assertIsNotNone(email)

    def test_can_return_error_when_invalid_address(self):
        invalid_email = "jan.kowalski"

        self.assertRaises(ValueError, EmailAddress, invalid_email)


if __name__ == "__main__":
 unittest.main()
