from sqlalchemy import Column, Integer, String
from .db import Base

class ItemORM(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
