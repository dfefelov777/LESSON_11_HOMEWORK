from sqlalchemy.orm import Session
from typing import List
from ..domain.models import Order, Product, Customer, Address
from ..domain.repositories import (
    ProductRepository,
    OrderRepository,
    CustomerRepository,
)
from .orm import ProductORM, OrderORM, CustomerORM, AddressORM


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product):
        product_orm = ProductORM(
            name=product.name, quantity=product.quantity, price=product.price
        )
        self.session.add(product_orm)
        self.session.flush()
        product.id = (
            product_orm.id
        )  # Обновляем доменную модель с ORM-сгенерированным ID

    def get(self, product_id: int) -> Product:
        product_orm = self.session.query(
            ProductORM).filter_by(id=product_id).one()
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price,
        )

    def list(self) -> List[Product]:
        products_orm = self.session.query(ProductORM).all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, customer: Customer):
        address_orm = AddressORM(
            street=customer.address.street,
            city=customer.address.city,
            state=customer.address.state,
            zip_code=customer.address.zip_code,
        )
        self.session.add(address_orm)
        self.session.flush()
        address_id = address_orm.id

        customer_orm = CustomerORM(
            name=customer.name,
            email=customer.email,
            address_id=address_id,
        )
        self.session.add(customer_orm)
        self.session.flush()
        customer.id = (
            customer_orm.id
        )  # Обновляем доменную модель с ORM-сгенерированным ID

    def get(self, customer_id: int) -> Customer:
        customer_orm = self.session.query(
            CustomerORM).filter_by(id=customer_id).one()
        address_orm = customer_orm.address
        address = Address(
            street=address_orm.street,
            city=address_orm.city,
            state=address_orm.state,
            zip_code=address_orm.zip_code,
        )
        return Customer(
            id=customer_orm.id,
            name=customer_orm.name,
            email=customer_orm.email,
            address=address,
            orders=[],  # Реализуйте получение заказов, если необходимо
        )

    def list(self) -> List[Customer]:
        customers_orm = self.session.query(CustomerORM).all()
        customers = []
        for customer_orm in customers_orm:
            address = Address(
                street=customer_orm.address.street,
                city=customer_orm.address.city,
                state=customer_orm.address.state,
                zip_code=customer_orm.address.zip_code,
            )
            customers.append(
                Customer(
                    id=customer_orm.id,
                    name=customer_orm.name,
                    email=customer_orm.email,
                    address=address,
                    orders=[],  # Реализуйте получение заказов, если необходимо
                )
            )
        return customers


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order):
        order_orm = OrderORM()
        order_orm.customer_id = order.customer.id
        order_orm.products = [
            self.session.query(ProductORM).filter_by(id=p.id).one()
            for p in order.products
        ]
        self.session.add(order_orm)
        self.session.flush()
        order.id = order_orm.id  # Обновляем доменную модель с ORM-сгенерированным ID

    def get(self, order_id: int) -> Order:
        order_orm = self.session.query(OrderORM).filter_by(id=order_id).one()
        customer_orm = order_orm.customer
        address = Address(
            street=customer_orm.address.street,
            city=customer_orm.address.city,
            state=customer_orm.address.state,
            zip_code=customer_orm.address.zip_code,
        )
        customer = Customer(
            id=customer_orm.id,
            name=customer_orm.name,
            email=customer_orm.email,
            address=address,
        )
        products = [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in order_orm.products
        ]
        return Order(id=order_orm.id, customer=customer, products=products)

    def list(self) -> List[Order]:
        orders_orm = self.session.query(OrderORM).all()
        orders = []
        for order_orm in orders_orm:
            customer_orm = order_orm.customer
            address = Address(
                street=customer_orm.address.street,
                city=customer_orm.address.city,
                state=customer_orm.address.state,
                zip_code=customer_orm.address.zip_code,
            )
            customer = Customer(
                id=customer_orm.id,
                name=customer_orm.name,
                email=customer_orm.email,
                address=address,
            )
            products = [
                Product(
                    id=p.id,
                    name=p.name,
                    quantity=p.quantity,
                    price=p.price)
                for p in order_orm.products
            ]
            orders.append(
                Order(
                    id=order_orm.id,
                    customer=customer,
                    products=products))
        return orders