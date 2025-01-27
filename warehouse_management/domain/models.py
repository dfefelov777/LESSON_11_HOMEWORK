from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str


@dataclass
class Customer:
    id: Optional[int]
    name: str
    email: str
    address: Address
    orders: List["Order"] = field(default_factory=list)


@dataclass
class Product:
    id: Optional[int]
    name: str
    quantity: int
    price: float


@dataclass
class Order:
    id: Optional[int]
    customer: Customer
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)