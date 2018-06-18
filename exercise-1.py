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




class Email:
    EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, str) or Email.EMAIL_PATTERN.match(value) is None:
            raise ValueError('Invalid email')
        self.value = value


class Person:
    email = Email()

    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class TestPersonEmailValidation(unittest.TestCase):
    def test_should_not_throw_exception_when_correct_mail_address_given(self):
        correct_mail = 'jan.kowalski@gmail.com'

        p = Person('Jan', 'Kowalski', correct_mail)

        self.assertEqual(p.email, correct_mail)

    def test_should_throw_exception_when_invalid_mail_given(self):
        incorrect_mails = [
            'jan.kowalski',
            '@gmail.com',
            23,
            dict(),
        ]

        for incorrect_mail in incorrect_mails:
            with self.subTest(email=incorrect_mail), self.assertRaises(ValueError):
                p = Person('Jan', 'Kowalski', incorrect_mail)


if __name__ == '__main__':
    unittest.main()
