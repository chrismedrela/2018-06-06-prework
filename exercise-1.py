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

EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class Email:
    def __init__(self, email_address):
        if EMAIL_PATTERN.match(email_address) is None:
            raise ValueError('Invalid email')
        else:
            self._email = email_address

    def get_address(self):
        return self._email


class Person(Email):
    def __init__(self, first_name, last_name, email):
        super(Person, self).__init__(email_address=email)
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)

        self._first_name = first_name
        self._last_name = last_name
        self._email = self.get_address()
