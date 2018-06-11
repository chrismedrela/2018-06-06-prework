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


class Customer:
    def __init__(self, first_purchase_date, birth_date, is_veteran):
        assert isinstance(first_purchase_date, (type(None), datetime.datetime))
        assert isinstance(birth_date, datetime.datetime)
        assert isinstance(is_veteran, bool)

        self.first_purchase_date = first_purchase_date
        self.birth_date = birth_date
        self.is_veteran = is_veteran


class AgeBasedDiscount:
    def __init__(self, age, value):
        self.min_age_in_years = age
        self.value = value
        self.now = datetime.datetime.now()
        self.year = datetime.timedelta(days=365)


class SeniorDiscount(AgeBasedDiscount):
    def applicable_discount(self, customer):
        if customer.birth_date <= self.now - (self.min_age_in_years * self.year):
            return self.value
        else:
            return 0


class LoyalDiscount(AgeBasedDiscount):
    def applicable_discount(self, customer):
        if customer.first_purchase_date is None:
            discount = 0
        elif customer.first_purchase_date <= self.now - (self.min_age_in_years * self.year):
            discount = self.value
        else:
            discount = 0
        return discount


class AttributeBasedDiscount:
    def __init__(self, value):
        self.value = value


class NewCustomerDiscount(AttributeBasedDiscount):
    def applicable_discount(self, customer):
        if customer.first_purchase_date is None:
            return self.value
        else:
            return 0


class VeteranDiscount(AttributeBasedDiscount):
    def applicable_discount(self, customer):
        if customer.is_veteran:
            return self.value
        else:
            return 0


def calculate_discount_percentage(customer):
    discounts = current_discounts()
    discounts = (discount.applicable_discount(customer) for discount in discounts)
    return max(discounts)


def current_discounts():
    discounts = [
        NewCustomerDiscount(value=15),
        VeteranDiscount(value=10),
        SeniorDiscount(age=65, value=5),
        LoyalDiscount(age=1, value=10),
        LoyalDiscount(age=5, value=12),
        LoyalDiscount(age=10, value=20)]
    return discounts


class CalculateDiscountPercentageTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.year = datetime.timedelta(days=365)

    def test_should_return_zero_for_casual_customer(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 0
        self.assertEqual(got, expected)

    def test_should_return_15_for_new_client(self):
        customer = Customer(first_purchase_date=None,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 15
        self.assertEqual(got, expected)

    def test_should_return_10_for_veteran(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now-20*self.year,
                            is_veteran=True)
        got = calculate_discount_percentage(customer)
        expected = 10
        self.assertEqual(got, expected)

    def test_should_return_5_for_a_senior(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now-65*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 5
        self.assertEqual(got, expected)

    def test_should_return_10_for_a_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now-1*self.year,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 10
        self.assertEqual(got, expected)

    def test_should_return_12_for_a_more_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now-5*self.year,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 12
        self.assertEqual(got, expected)

    def test_should_return_20_for_a_most_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now-10*self.year,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 20
        self.assertEqual(got, expected)

    def test_should_return_maximum_discount(self):
        customer = Customer(first_purchase_date=None,
                            birth_date=self.now-20*self.year,
                            is_veteran=True)
        # eligible for 15% discount as a new client and 10% as a veteran
        got = calculate_discount_percentage(customer)
        expected = 15
        self.assertEqual(got, expected)

if __name__ == "__main__":
    unittest.main()
