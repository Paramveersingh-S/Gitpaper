from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    version = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    repository = relationship("Repository")
