from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .orm import Base

DATABASE_URL = "postgresql://USER:123456@db:5432/warehouse_HOMEWORK"
