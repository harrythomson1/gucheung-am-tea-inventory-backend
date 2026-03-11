from uuid import UUID

from pydantic import BaseModel, model_validator

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

    @model_validator(mode="after")
    def validate_transaction_fields(self):
        if self.transaction_type == TransactionType.harvest:
            if not self.tea_name:
                raise ValueError("tea_name is required for harvest transactions")
            if not self.packaging:
                raise ValueError("packaging is required for harvest transactions")
            if not self.flush:
                raise ValueError("flush is required for harvest transactions")
            if not self.harvest_year:
                raise ValueError("harvest_year is required for harvest transactions")
            if not self.unit:
                raise ValueError("unit is required for harvest transactions")
            if self.quantity_change <= 0:
                raise ValueError(
                    "quantity_change must be positive for harvest transactions"
                )
        else:
            if not self.tea_variant_id:
                raise ValueError(
                    "tea_variant_id is required for non-harvest transactions"
                )
            if self.quantity_change >= 0:
                raise ValueError(
                    "quantity_change must be negative for non-harvest transactions"
                )
        return self
