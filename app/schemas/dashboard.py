from pydantic import BaseModel


class DashboardTeaResponse(BaseModel):
    tea_id: int
    tea_name: str
    total_stock: int

    model_config = {"from_attributes": True}
