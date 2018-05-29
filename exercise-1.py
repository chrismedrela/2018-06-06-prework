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


EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class Email:
    def __init__(self, address):
        assert isinstance(address, str)

        if EMAIL_PATTERN.match(address) is None:
            raise ValueError('Invalid email')
        else:
            self.address = address


class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, Email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email


import pprint
pp = pprint.PrettyPrinter(indent=4)

ja = Person('Artur', 'Smolinski', Email('smolkia.com'))

pp.pprint(ja)
pp.pprint(ja.first_name + ' ' + ja.last_name + ' ' + str(ja.email.address))
