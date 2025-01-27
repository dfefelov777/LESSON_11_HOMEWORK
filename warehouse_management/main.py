from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import (
    SqlAlchemyProductRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyCustomerRepository,
)
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL
from domain.models import Address

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    uow = SqlAlchemyUnitOfWork(SessionFactory)
    with uow:
        product_repo = SqlAlchemyProductRepository(uow.session)
        order_repo = SqlAlchemyOrderRepository(uow.session)
        customer_repo = SqlAlchemyCustomerRepository(uow.session)

        warehouse_service = WarehouseService(
            product_repo, order_repo, customer_repo)

        address = Address(
            street="Ленина 13",
            city="Лобня",
            state="Московская область",
            zip_code="141730",
        )
        customer = warehouse_service.create_customer(
            name="Вася Пупкин", email="vasya.pupkin@example.com", address=address
        )
        print(f"Создан покупатель: {customer}")

        new_product = warehouse_service.create_product(
            name="IPhone", quantity=10, price=100550.99
        )
        print(f"Создан продукт: {new_product}")

        # Create an order
        order = warehouse_service.create_order(
            customer=customer, products=[new_product]
        )
        print(f"Создан заказ: {order}")


if __name__ == "__main__":
    main()