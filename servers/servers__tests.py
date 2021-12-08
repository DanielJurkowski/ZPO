# Grupa 2a: Jurkowski 40720, Jarzyna ..., Janik ...
import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError, Server

server_types = MapServer, ListServer


"""
Czy wyniki zwrócone przez serwer przechowujący dane w liście są poprawnie posortowane?
- test_get_entries_returns_proper_entries

Czy przekroczenie maksymalnej liczby znalezionych produktów powoduje rzucenie wyjątku? 
- test_get_entries_raises_exceptions_if_too_many_results

Czy funkcja obliczająca łączną cenę produktów zwraca poprawny wynik w przypadku rzucenia wyjątku oraz braku produktów 
pasujących do kryterium wyszukiwania? - test_total_price_for_normal_execution / 
test_total_price_is_zero_if_exception_raised / test_total_price_is_zero_if_does_not_meet_conditions 
"""


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]

        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)

            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_raises_exceptions_if_too_many_results(self):
        products = [Product('PP12', 1), Product('PP234', 2), Product('PP235', 1), Product('PP225', 1)]

        for server_type in server_types:
            server = server_type(products)

            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]

        for server_type in server_types:
            server = server_type(products)
            client = Client(server)

            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_is_none_if_exception_raised(self):
        products = [Product('PP234', 2), Product('PP275', 3),  Product('PP215', 3),  Product('PP235', 3)]

        for server_type in server_types:
            server = server_type(products)
            client = Client(server)

            self.assertIsNone(client.get_total_price(2))

    def test_total_price_is_none_if_does_not_meet_conditions(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]

        for server_type in server_types:
            server = server_type(products)
            client = Client(server)

            self.assertIsNone(client.get_total_price(3))


class ProductTest(unittest.TestCase):
    def test_product_value_error(self):
        with self.assertRaises(ValueError):
            products = [Product('1999', 1)]


if __name__ == '__main__':
    unittest.main()
