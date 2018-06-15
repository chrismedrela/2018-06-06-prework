# encoding: utf-8

"""
Open Close Principle to jedna z pięciu zasad SOLID. Mówi ona, że klasy i funkcje
powinny być otwarte na rozszerzenie i zamknięte na modyfikacje. Innymi słowy,
powinno być możliwe ponowne wykorzystanie kodu bez modyfikowania go.

Poniżej znajduje się funkcja `calculate_discount_percentage`, która jest pewną
strategią wyliczania przysługującej klientowi zniżki wyrażonej w procentach.
Każdy klient jest instancją klasy Customer i ma trzy pola:

- first_purchase_date -- data pierwszego zakupu lub None, jeżeli jest to nowy
  klient
- birth_date -- data urodzenia
- is_veteran -- flaga informująca, czy dany klient jest VIPem

Zaimplementowano następującą strategię:

- seniorzy (65+) dostają 5% zniżki
- lojalni klienci, którzy są z nami od 1, 5 lub 10 lat, dostają odpowiednio 10%,
  12% i 20% zniżki,
- nowi klienci dostają 15% zniżki
- veterani dostają 10% zniżki
- pozostali dostają 0% zniżki
- jeżeli przysługuje więcej niż jedna zniżka, zniżki nie sumują się i wybieramy
  tę największą

Dodatkowo, niżej widzimy testy jednostkowe tej funkcji.

W tej funkcji złamano zasadę otwarte-zamknięte, ponieważ nie ma możliwości
ponownego wykorzystania jej.

Jako ćwiczenie, postaraj się zrefaktoryzować kod tak, aby możliwe było ponowne
użycie fragmentów obecnej strategii. Innymi słowy, powinno być możliwe
zaimplementowanie podobnej strategii (w której, przykładowo, nie ma zniżki dla
nowych klientów), bez duplikowania kodu.
"""

import datetime
import unittest
from collections import OrderedDict


class Date(object):
    @classmethod
    def now(cls):
        return datetime.datetime.now()

    @classmethod
    def year(cls):
        return datetime.timedelta(days=365)


def get_years_delta(years=1):
    return Date.now() - years * Date.year()


class Customer(object):
    loyalty_discount_map = OrderedDict(((10, 20), (5, 12), (1, 10)))
    senior_discount_percentage = 5
    new_customer_discount_percentage = 15
    veteran_discount_percentage = 10

    def __init__(self, first_purchase_date, birth_date, is_veteran):
        assert isinstance(first_purchase_date, (type(None), datetime.datetime))
        assert isinstance(birth_date, datetime.datetime)
        assert isinstance(is_veteran, bool)

        self.first_purchase_date = first_purchase_date
        self.birth_date = birth_date
        self.is_veteran = is_veteran

    @property
    def loyalty_discount(self):
        if not self.first_purchase:
            for years, discount in self.loyalty_discount_map.items():
                if self.first_purchase_date <= get_years_delta(years):
                    return discount
        return 0

    @property
    def new_customer_discount(self):
        if self.first_purchase:
            return self.new_customer_discount_percentage
        else:
            return 0

    @property
    def first_purchase(self):
        return self.first_purchase_date is None

    @property
    def veteran_discount(self):
        if self.is_veteran:
            return self.veteran_discount_percentage
        else:
            return 0

    @property
    def senior_discount(self):
        if self.have_senior_discount():
            return self.senior_discount_percentage
        else:
            return 0

    def have_senior_discount(self):
        return self.birth_date <= get_years_delta(65)


def calculate_discount_percentage(customer):
    return max(customer.loyalty_discount, customer.veteran_discount, customer.senior_discount,
               customer.new_customer_discount)


class CalculateDiscountPercentageTests(unittest.TestCase):
    def setUp(self):
        self.now = Date.now()
        self.year = Date.year()

    def test_should_return_zero_for_casual_customer(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 0
        self.assertEqual(got, expected)

    def test_should_return_15_for_new_client(self):
        customer = Customer(first_purchase_date=None,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 15
        self.assertEqual(got, expected)

    def test_should_return_10_for_veteran(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=True)
        got = calculate_discount_percentage(customer)
        expected = 10
        self.assertEqual(got, expected)

    def test_should_return_5_for_a_senior(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now - 65 * self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 5
        self.assertEqual(got, expected)

    def test_should_return_10_for_a_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now - 1 * self.year,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 10
        self.assertEqual(got, expected)

    def test_should_return_12_for_a_more_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now - 5 * self.year,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 12
        self.assertEqual(got, expected)

    def test_should_return_20_for_a_most_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now - 10 * self.year,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 20
        self.assertEqual(got, expected)

    def test_should_return_maximum_discount(self):
        customer = Customer(first_purchase_date=None,
                            birth_date=self.now - 20 * self.year,
                            is_veteran=True)
        # eligible for 15% discount as a new client and 10% as a veteran
        got = calculate_discount_percentage(customer)
        expected = 15
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
