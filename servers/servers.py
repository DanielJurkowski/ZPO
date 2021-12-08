# Grupa 2a: Jurkowski 40720, Jarzyna ..., Janik ...
from typing import Optional, List, Dict, TypeVar
from abc import ABC, abstractmethod
import re


class Product:
    def __init__(self, name: str, price: float) -> None:
        pattern = "^[a-zA-Z]+[0-9]+$"

        if re.fullmatch(pattern, name):
            self.name: str = name
            self.price: float = price

        else:
            raise ValueError

    def __members(self):
        return self.name, self.price

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False

    def __hash__(self):
        return hash(self.__members())


class TooManyProductsFoundError(Exception):
    pass


class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def get_product_list(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pattern = '^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$'.format(n_letters=n_letters)
        entries = [p for p in self.get_product_list(n_letters)
                   if re.match(pattern, p.name)]

        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError

        return sorted(entries, key=lambda entry: entry.price)


ServerType = TypeVar('ServerType')


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: List[Product] = products

    def get_product_list(self, n_letters: int = 1) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {p.name: p.price for p in products}

    def get_product_list(self, n_letters: int = 1) -> List[Product]:
        return list(Product(k, v) for k, v in self.products.items())


class Client:
    def __init__(self, server: ServerType) -> None:
        self.server: ServerType = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            entries = self.server.get_entries() if n_letters is None else self.server.get_entries(n_letters)

            if not entries:
                return None

            else:
                return sum([entry.price for entry in entries])

        except TooManyProductsFoundError:
            return None
