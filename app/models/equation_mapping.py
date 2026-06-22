from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class EquationMapping(Base):
    __tablename__ = "equation_mappings"

    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    commit_sha = Column(String, nullable=False)
    file_path = Column(String, nullable=False)       # e.g. "models/attention.py"
    line_start = Column(Integer, nullable=True)
    line_end = Column(Integer, nullable=True)
    equation_label = Column(String, nullable=False)  # e.g. "eq:3.1"
    description = Column(Text, nullable=True)        # from commit message
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    paper = relationship("Paper", back_populates="equation_mappings")
    repository = relationship("Repository", back_populates="equation_mappings")
