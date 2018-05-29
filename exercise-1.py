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


EMAIL_PATTERN = re.compile(
    r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class Email:
    def __init__(self, email):
        self.email = self.validate(email)

    def __str__(self):
        return self.email

    @staticmethod
    def validate(email):
        assert isinstance(email, str)

        if EMAIL_PATTERN.match(email) is None:
            raise ValueError('Invalid email')
        else:
            return email


class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)

        self.first_name = first_name
        self.last_name = last_name
        # zajebiscie bo mamy _email, ktory dodatkowo jest tworzony w locie...
        self.email = email

    @property
    def email(self):
        return str(self._email)

    @email.setter
    def email(self, new_email):
        self._email = Email(new_email)


class TestPerson(unittest.TestCase):
    def test_should_create_person_instance(self):
        p = Person('Ala', 'Makota', 'alamakota@gmail.com')

        self.assertEqual(p.first_name, 'Ala')
        self.assertEqual(p.last_name, 'Makota')
        self.assertEqual(p.email, 'alamakota@gmail.com')

    def test_should_raise_value_error_invalid_email(self):
        self.assertRaises(ValueError, Person, 'Ala', 'Makota', 'zly-email')


if __name__ == '__main__':
    unittest.main()
