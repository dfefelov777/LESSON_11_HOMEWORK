import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..")))

import pytest
from unittest.mock import Mock
from ...domain.services import WarehouseService
from ...domain.models import Product, Customer, Address


def test_create_product():
    product_repo = Mock()
    order_repo = Mock()
    customer_repo = Mock()
    service = WarehouseService(product_repo, order_repo, customer_repo)

    product = service.create_product(
        name="Некий продукт", quantity=5, price=1000.05)

    product_repo.add.assert_called_once()
    assert product.name == "Некий продукт"
    assert product.quantity == 5
    assert product.price == 1000.05


def test_create_customer():
    product_repo = Mock()
    order_repo = Mock()
    customer_repo = Mock()
    service = WarehouseService(product_repo, order_repo, customer_repo)

    address = Address("Гагарина 5", "Клин", "Московская область", "141600")
    customer = service.create_customer(
        name="Петя Камушкин", email="petya@example.com", address=address
    )

    customer_repo.add.assert_called_once()
    assert customer.name == "Петя Камушкин"
    assert customer.email == "petya@example.com"
    assert customer.address == address