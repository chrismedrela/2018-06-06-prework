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


class Email:
    EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')
    
    def __init__(self, email):
        if self.EMAIL_PATTERN.match(email) is None:
            raise ValueError('Invalid email')
        else:
            self.email = email
        

class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, Email)
        
        self.first_name = first_name 
        self.last_name = last_name
        self.email = email
