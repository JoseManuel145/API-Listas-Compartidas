from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.Infrastructure.db.db import Base
from sqlalchemy.orm import relationship

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True)
    list_id = Column(String(36), ForeignKey("shared_lists.id"), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=False), nullable=False)

    lista = relationship("SharedListTable", back_populates="productos")
