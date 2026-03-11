from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship

class Tea(Base):
    __tablename__ = "teas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tea_variants = relationship("TeaVariant", back_populates="tea")
