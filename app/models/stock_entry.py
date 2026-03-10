import enum
from sqlalchemy import Column, Integer, Enum, DateTime, func, ForeignKey, Date
from core.database import Base
from sqlalchemy.orm import relationship

class PackagingType(enum.Enum):
    foil = "foil"
    wing = "wing"
    gift = "gift"

class UnitType(enum.Enum):
    grams = "grams"
    bags = "bags"

class FlushType(enum.Enum):
    first = "first"
    second = "second"

class TeaVariant(Base):
    __tablename__ = "tea_variants"

    id = Column(Integer, primary_key=True, index=True)
    tea_id = Column(Integer, ForeignKey("teas.id"), nullable=False)
    packaging_type = Column(Enum(PackagingType, name="packaging_type"), nullable=False)
    unit = Column(Enum(UnitType, name="unit"), nullable=False)
    flush = Column(Enum(FlushType, name="flush_type"), nullable=False)
    harvest_year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tea = relationship("Tea", back_populates="tea_variants")
    stock_transactions = relationship("StockTransaction", back_populates="tea_variant")
