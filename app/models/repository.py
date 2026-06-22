from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    installation_id = Column(Integer, ForeignKey("installations.id"), nullable=False)
    owner = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    papers = relationship("Paper", back_populates="repository")
    equation_mappings = relationship("EquationMapping", back_populates="repository")
