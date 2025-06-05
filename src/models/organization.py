from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.database import Base

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    org_name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    phone_number = Column(VARCHAR(20), nullable=True)
    industry = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    gst_number = Column(VARCHAR(40), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="organization", lazy="selectin")

