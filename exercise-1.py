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
    
    _email_pattern = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')

    def __new__(self, email: str):
        checked = self._email_pattern.search(email)
        return self.check(checked)

    
    @staticmethod
    def check(email: str) -> str:
        if not email:
            raise ValueError('Invalid email')
            
        return email[0]



class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)
        
        self.first_name = first_name 
        self.last_name = last_name
        self.email = Email(email)
