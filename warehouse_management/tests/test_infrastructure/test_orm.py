import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..")))

import pytest
from ...infrastructure.orm import Base, ProductORM, CustomerORM, AddressORM, OrderORM
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    return engine


@pytest.fixture(scope="session")
def setup_database(engine):
    Base.metadata.create_all(engine)


@pytest.fixture
def session(engine, setup_database):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute(text("PRAGMA foreign_keys=ON"))
    yield session
    session.close()


@pytest.fixture
def address_orm(session):
    address = AddressORM(
        street="Test Street", city="Test City", state="TS", zip_code="12345"
    )
    session.add(address)
    session.commit()
    return address


@pytest.fixture
def customer_orm(session, address_orm):
    customer = CustomerORM(
        name="Test Customer", email="customer@test.com", address_id=address_orm.id
    )
    session.add(customer)
    session.commit()
    return customer


@pytest.fixture
def products_orm(session):
    product1 = ProductORM(name="Product 1", quantity=5, price=10.0)
    product2 = ProductORM(name="Product 2", quantity=3, price=20.0)
    session.add_all([product1, product2])
    session.commit()
    return [product1, product2]


def test_product_orm(session):
    product = ProductORM(name="Test Product", quantity=12, price=199.99)
    session.add(product)
    session.commit()

    retrieved_product = session.query(
        ProductORM).filter_by(name="Test Product").one()
    assert retrieved_product.quantity == 12
    assert retrieved_product.price == 199.99


def test_customer_and_address_orm(session, customer_orm):
    retrieved_customer = (
        session.query(CustomerORM).filter_by(name="Test Customer").one()
    )
    assert retrieved_customer.email == "customer@test.com"
    assert retrieved_customer.address.city == "Test City"


def test_order_orm(session, customer_orm, products_orm):
    order = OrderORM(customer_id=customer_orm.id)
    order.products.extend(products_orm)
    session.add(order)
    session.commit()

    retrieved_order = session.query(OrderORM).filter_by(id=order.id).one()
    assert retrieved_order.customer.name == "Test Customer"
    assert len(retrieved_order.products) == 2
    product_names = [p.name for p in retrieved_order.products]
    assert "Product 1" in product_names
    assert "Product 2" in product_names