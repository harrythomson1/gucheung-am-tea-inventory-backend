from datetime import datetime

from pydantic import BaseModel


class CreateCustomerRequest(BaseModel):
    name: str
    city: str
    address: str | None = None
    phone: str | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class CustomerResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str | None = None
    phone: str | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateCustomerRequest(BaseModel):
    name: str | None = None
    city: str | None = None
    address: str | None = None
    phone: str | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}
