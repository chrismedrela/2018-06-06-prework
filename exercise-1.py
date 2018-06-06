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


class Email(str):
    email_pattern = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')
    def __new__(cls, email):
        if cls.email_pattern.match(email) is None:
            raise ValueError('Invalid email')
        return email
    

class Person:
    def __init__(self, first_name, last_name, email):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)
        
        self.first_name = first_name 
        self.last_name = last_name
        self.email = Email(email)

class PersonTests(unittest.TestCase):
    def test_should_pass(self):
        p = Person("Name", "Name", "name@name.com")
        
    def test_should_raise_on_space_instead_of_at(self):
        with self.assertRaises(ValueError):
            Person("name", "name", "name name.com")
    
    def test_should_raise_on_missing_domain(self):
        with self.assertRaises(ValueError):
            Person("name", "name", "name@name")
    
    def test_should_raise_on_missing_email(self):
        with self.assertRaises(ValueError):
            Person("name", "name", "")
