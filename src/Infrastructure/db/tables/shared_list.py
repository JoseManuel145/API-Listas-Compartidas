from sqlalchemy import Column, String, DateTime
from src.Infrastructure.db.db import Base
from sqlalchemy.orm import relationship

class SharedListTable(Base):
    __tablename__ = "shared_lists"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=False), nullable=False)

    
    productos = relationship(
        "ProductTable", 
        back_populates="lista",
        cascade="all, delete-orphan"
    )