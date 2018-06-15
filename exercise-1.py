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


class InvalidEmail(Exception):
    pass


class Email(object):
    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return self.email_address

    def _validate_mail(self):
        if EMAIL_PATTERN.match(self.email_address) is None:
            raise InvalidEmail('Invalid email')

    @property
    def validated(self):
        self._validate_mail()
        return self


class Person(object):
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, Email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email.validated

    def __repr__(self):
        return "Name: {name}\nSurname: {surname}\nMail: {mail}".format(name=self.first_name, surname=self.last_name,
                                                                       mail=self.email)
