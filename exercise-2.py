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

import abc
import typing
import datetime
import unittest

class Customer:

    def __init__(self, first_purchase_date, birth_date, is_veteran):

        assert isinstance(first_purchase_date, (type(None), datetime.datetime))
        assert isinstance(birth_date, datetime.datetime)
        assert isinstance(is_veteran, bool)

        self.first_purchase_date = first_purchase_date
        self.birth_date = birth_date
        self.is_veteran = is_veteran

class AbstractDiscount(metaclass = abc.ABCMeta):

    @abc.abstractmethod
    def __new__(cls, customer: Customer):

        return 0

class SeniorDiscount(AbstractDiscount):

    def __new__(cls, customer: Customer):

        now = datetime.datetime.now()
        year = datetime.timedelta(days = 365)

        if customer.birth_date <= now - 65 * year:
            return 5

        return 0

class OneYearLoyalCustomerDiscount(AbstractDiscount):

    def __new__(cls, customer: Customer):

        now = datetime.datetime.now()
        year = datetime.timedelta(days = 365)

        if customer.first_purchase_date is None:
            return 0

        if customer.first_purchase_date <= now - year:
            return 10

        return 0

class FiveYearLoyalCustomerDiscount(AbstractDiscount):

    def __new__(cls, customer: Customer):

        now = datetime.datetime.now()
        year = datetime.timedelta(days = 365)

        if customer.first_purchase_date is None:
            return 0

        if customer.first_purchase_date <= now - 5 * year:
            return 12

        return 0

class TenYearLoyalCustomerDiscount(AbstractDiscount):

    def __new__(cls, customer: Customer):

        now = datetime.datetime.now()
        year = datetime.timedelta(days = 365)

        if customer.first_purchase_date is None:
            return 0

        if customer.first_purchase_date <= now - 10 * year:
            return 20

        return 0

class FirstTimePurchaseDiscount(AbstractDiscount):

    def __new__(cls, customer: Customer):

        if customer.first_purchase_date is None:
            return 15

        return 0

class VeteranDiscount(AbstractDiscount):

    def __new__(cls, customer: Customer):

        if customer.is_veteran:
            return 10

        return 0

class DiscountCalculator:

    def __init__(self, functors: typing.List[type(AbstractDiscount)] = None):

        self._functors = functors if functors is not None else []

        assert all(issubclass(f, AbstractDiscount) for f in self._functors)

    def calculate(self, customer):

        assert isinstance(customer, Customer)

        discounts = []

        for functor in self._functors:
            discounts.append(functor(customer))

        return max(discounts)

class CalculateDiscountPercentageTests(unittest.TestCase):

    def setUp(self):

        self.now = datetime.datetime.now()
        self.year = datetime.timedelta(days = 365)

        self.functors = [
            SeniorDiscount,
            OneYearLoyalCustomerDiscount,
            FiveYearLoyalCustomerDiscount,
            TenYearLoyalCustomerDiscount,
            FirstTimePurchaseDiscount,
            VeteranDiscount,
        ]

    def test_should_return_zero_for_casual_customer(self):

        customer = Customer(
            first_purchase_date = self.now,
            birth_date = self.now - 20 * self.year,
            is_veteran = False
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 0

        self.assertEqual(got, expected)

    def test_should_return_15_for_new_client(self):

        customer = Customer(
            first_purchase_date = None,
            birth_date = self.now - 20 * self.year,
            is_veteran = False
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 15

        self.assertEqual(got, expected)

    def test_should_return_10_for_veteran(self):

        customer = Customer(
            first_purchase_date = self.now,
            birth_date = self.now - 20 * self.year,
            is_veteran = True
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 10

        self.assertEqual(got, expected)

    def test_should_return_5_for_a_senior(self):

        customer = Customer(
            first_purchase_date = self.now,
            birth_date = self.now - 65 * self.year,
            is_veteran = False
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 5

        self.assertEqual(got, expected)

    def test_should_return_10_for_a_loyal_customer(self):

        customer = Customer(
            first_purchase_date = self.now - 1 * self.year,
            birth_date = self.now - 20 * self.year,
            is_veteran = False
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 10

        self.assertEqual(got, expected)

    def test_should_return_12_for_a_more_loyal_customer(self):

        customer = Customer(
            first_purchase_date = self.now - 5 * self.year,
            birth_date = self.now - 20 * self.year,
            is_veteran = False
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 12

        self.assertEqual(got, expected)

    def test_should_return_20_for_a_most_loyal_customer(self):

        customer = Customer(
            first_purchase_date = self.now - 10 * self.year,
            birth_date = self.now - 20 * self.year,
            is_veteran = False
        )

        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 20

        self.assertEqual(got, expected)

    def test_should_return_maximum_discount(self):

        customer = Customer(
            first_purchase_date = None,
            birth_date = self.now - 20 * self.year,
            is_veteran = True
        )

        # eligible for 15% discount as a new client and 10% as a veteran
        got = DiscountCalculator(self.functors).calculate(customer)
        expected = 15

        self.assertEqual(got, expected)

if __name__ == "__main__":
    unittest.main()
