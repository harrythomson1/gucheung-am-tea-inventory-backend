from enums import PackagingType
from pydantic import BaseModel


class DashboardTeaResponse(BaseModel):
    id: int
    name: str
    packaging: PackagingType
    total_stock: int

    model_config = {"from_attributes": True}
