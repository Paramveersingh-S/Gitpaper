from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Installation(Base):
    __tablename__ = "installations"

    id = Column(Integer, primary_key=True)
    installation_id = Column(Integer, unique=True, nullable=False, index=True)
    account_login = Column(String, nullable=False)  # org or user name
    account_type = Column(String, nullable=False)   # "Organization" or "User"
    access_tokens_url = Column(String)
    is_active = Column(Boolean, default=True)
    installed_at = Column(DateTime(timezone=True), server_default=func.now())
    uninstalled_at = Column(DateTime(timezone=True), nullable=True)
