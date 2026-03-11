from uuid import UUID

from pydantic import BaseModel

from app.enums import (
    FlushType,
    PackagingType,
    SalesChannelType,
    TransactionType,
    UnitType,
)


class CreateTransactionRequest(BaseModel):
    transaction_type: TransactionType
    tea_name: str | None = None
    tea_variant_id: int | None = None
    packaging: PackagingType | None = None
    unit: UnitType | None = None
    flush: FlushType | None = None
    harvest_year: int | None = None
    quantity_change: int
    performed_by_id: UUID
    performed_by_name: str
    buyer_name: str | None = None
    buyer_phone: str | None = None
    sales_channel: SalesChannelType | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}
