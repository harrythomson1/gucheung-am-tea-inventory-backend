from pydantic import BaseModel


class DashboardTeaResponse(BaseModel):
    id: int
    name: str
    total_stock: int

    model_config = {"from_attributes": True}
