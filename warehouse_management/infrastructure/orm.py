from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AddressORM(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)


class CustomerORM(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address = relationship("AddressORM")
    orders = relationship(
        "OrderORM",
        back_populates="customer",
        cascade="all, delete-orphan",
    )


class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)


class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.id",
            ondelete="CASCADE"))
    customer = relationship("CustomerORM", back_populates="orders")
    products = relationship("ProductORM",
                            secondary="order_product_associations")


order_product_associations = Table(
    "order_product_associations",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id", ondelete="CASCADE")),
    Column("product_id", Integer, ForeignKey("products.id")),
)