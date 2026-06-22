from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    arxiv_id = Column(String, nullable=True)        # e.g. "1706.03762"
    doi = Column(String, nullable=True)
    title = Column(String, nullable=False)
    authors = Column(JSON, nullable=True)            # list of author names
    abstract = Column(Text, nullable=True)
    pdf_url = Column(String, nullable=True)
    published_date = Column(DateTime(timezone=True), nullable=True)
    equations = Column(JSON, nullable=True)          # parsed equation labels
    linked_at = Column(DateTime(timezone=True), server_default=func.now())
    added_by = Column(String, nullable=True)         # GitHub username

    repository = relationship("Repository", back_populates="papers")
    equation_mappings = relationship("EquationMapping", back_populates="paper")
