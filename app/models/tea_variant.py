from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums import FlushType, PackagingType


class TeaVariant(Base):
    __tablename__ = "tea_variants"
    __table_args__ = (
        UniqueConstraint(
            "tea,id",
            "packaging",
            "flush",
            "harvest_year",
            "weight_grams",
            name="uq_tea_variant",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    tea_id = Column(Integer, ForeignKey("teas.id"), nullable=False)
    packaging = Column(Enum(PackagingType, name="packaging_type"), nullable=False)
    flush = Column(Enum(FlushType, name="flush_type"), nullable=False)
    harvest_year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    weight_grams = Column(Integer, nullable=False)

    tea = relationship("Tea", back_populates="tea_variants")
    stock_transactions = relationship("StockTransaction", back_populates="tea_variant")
