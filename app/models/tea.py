from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Tea(Base):
    __tablename__ = "teas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    deleted = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tea_variants = relationship("TeaVariant", back_populates="tea")
