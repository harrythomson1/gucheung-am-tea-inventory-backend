from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums import SalesChannelType, TransactionType


class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True, index=True)
    tea_variant_id = Column(Integer, ForeignKey("tea_variants.id"), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    transaction_type = Column(
        Enum(TransactionType, name="transaction_type"), nullable=False
    )
    performed_by_id = Column(UUID(as_uuid=True), nullable=False)
    performed_by_name = Column(String, nullable=False)
    buyer_name = Column(String, nullable=True)
    buyer_phone = Column(String, nullable=True)
    sales_channel = Column(
        Enum(SalesChannelType, name="sales_channel_type"), nullable=True
    )
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tea_variant = relationship("TeaVariant", back_populates="stock_transactions")
