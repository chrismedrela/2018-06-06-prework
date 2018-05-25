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

    __slots__ = ['_value']

    def __init__(self, value: str):

        self.value = value

    @property
    def value(self) -> str:

        return self._value

    @value.setter
    def value(self, value: str) -> None:

        assert isinstance(value, str)

        if re.match(self.pattern, value) is None:
            raise ValueError('Invalid email')

        self._value = value

    @property
    def pattern(self) -> str:

        return r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$'

class Person:

    __slots__ = ['first_name', 'last_name', '_email']

    def __init__(self, first_name: str, last_name: str, email: str):

        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)

        self.first_name = first_name
        self.last_name = last_name

        self._email = Email(email)

    @property
    def email(self) -> str:

        return self._email.value

    @email.setter
    def email(self, value: str) -> None:

        self._email.value = value
