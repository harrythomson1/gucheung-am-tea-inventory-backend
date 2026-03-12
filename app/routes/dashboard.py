from fastapi import APIRouter, Depends

from app.dependencies import get_teas_service
from app.schemas import DashboardTeaResponse
from app.services.tea_service import TeaService

router = APIRouter()


@router.get("/dashboard", response_model=list[DashboardTeaResponse])
async def get_stock_summary(service: TeaService = Depends(get_teas_service)):
    stock_summary = await service.get_stock_summary()
    return stock_summary
