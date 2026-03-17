from datetime import datetime

from pydantic import BaseModel

from app.enums import FlushType, PackagingType


class TeaResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TeaVariantResponse(BaseModel):
    id: int
    packaging: PackagingType
    flush: FlushType
    harvest_year: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TeaDetailResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    tea_variants: list[TeaVariantResponse] = []

    model_config = {"from_attributes": True}


class TeaVariantStockResponse(BaseModel):
    id: int
    tea_name: str
    packaging: PackagingType
    flush: FlushType
    harvest_year: int
    weight_grams: int
    current_stock: int

    model_config = {"from_attributes": True}


class CreateTeaRequest(BaseModel):
    name: str
