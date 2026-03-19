from datetime import datetime

from pydantic import BaseModel

from app.enums import FlushType, PackagingType, SalesChannelType, TransactionType


class ActivityFeedResponse(BaseModel):
    quantity_change: int
    transaction_type: TransactionType
    performed_by_name: str
    sales_channel: SalesChannelType | None = None
    notes: str | None = None
    packaging: PackagingType
    flush: FlushType
    harvest_year: int
    weight_grams: int
    tea_name: str
    created_at: datetime

    model_config = {"from_attributes": True}
