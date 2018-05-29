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


class Mail:
    EMAIL_PATERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')
    def __init__(self, mail):
        assert isinstance(mail, str)
        self._mail = mail
    
    @property
    def mail(self):
        if self.EMAIL.PATERN.math(self._mail) is None:
            raise ValueError('Wrong email')
        else:
            return self._mail

class Person:
    def __init__(self, first_name, last_name, mail):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        
        self.first_name = first_name 
        self.last_name = last_name
        self.mail = Mail(mail).mail
