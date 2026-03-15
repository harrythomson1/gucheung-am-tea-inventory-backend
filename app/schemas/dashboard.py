from pydantic import BaseModel

from app.enums import PackagingType


class DashboardTeaResponse(BaseModel):
    id: int
    name: str
    packaging: PackagingType
    harvest_year: int
    total_stock: int

    model_config = {"from_attributes": True}
