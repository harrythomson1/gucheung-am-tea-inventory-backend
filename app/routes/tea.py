from fastapi import APIRouter, Depends
from app.dependencies import get_teas_service
from app.services.tea_service import TeaService

router = APIRouter()

@router.get("/teas")
async def get_all_teas(
    service: TeaService = Depends(get_teas_service)
):
    return await service.get_all()
