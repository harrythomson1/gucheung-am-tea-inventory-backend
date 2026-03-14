from pydantic import BaseModel

from app.enums import PackagingType


class DashboardTeaResponse(BaseModel):
    id: int
    name: str
    packaging: PackagingType
    total_stock: int

    model_config = {"from_attributes": True}
