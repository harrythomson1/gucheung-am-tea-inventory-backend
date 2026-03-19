from fastapi import APIRouter, Depends

from app.auth.utils import get_current_user
from app.dependencies import get_teas_service
from app.schemas import DashboardTeaResponse
from app.services import TeaService

router = APIRouter()


@router.get("/dashboard", response_model=list[DashboardTeaResponse])
async def get_stock_summary(
    _: dict = Depends(get_current_user), service: TeaService = Depends(get_teas_service)
):
    stock_summary = await service.get_stock_summary()
    return stock_summary
