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

class EmailValidatorMeta(type):

    def __setattr__(self, key, value):

        if key == '__pattern__':
            raise AttributeError('Cannot change pattern value')

        super().__setattr__(key, value)

class EmailValidator(metaclass = EmailValidatorMeta):

    __slots__ = ['_value']

    __pattern__ = re.compile(
        r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$'
    )

    def __new__(cls, email: str) -> str:

        assert isinstance(email, str)

        if re.match(cls.__pattern__, email) is None:
            raise ValueError('Invalid email')

        return email

class Person:

    __slots__ = ['first_name', 'last_name', 'email']

    def __init__(self, first_name: str, last_name: str, email: str):

        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)

        self.first_name = first_name
        self.last_name = last_name
        self.email = EmailValidator(email)

class EmailValidationTests(unittest.TestCase):

    def setUp(self):

        self.first_name = 'Jan'
        self.last_name = 'Kowalski'

    def test_no_name_before_monkey(self):

        with self.assertRaises(ValueError):
            Person(self.first_name, self.last_name, '@gmail.com')

    def test_space_instead_of_monkey(self):

        with self.assertRaises(ValueError):
            Person(self.first_name, self.last_name, 'jan.kowalski gmail.com')

    def test_no_domain_after_monkey(self):

        with self.assertRaises(ValueError):
            Person(self.first_name, self.last_name, 'jan.kowalski@gmail')

if __name__ == "__main__":
    unittest.main()
