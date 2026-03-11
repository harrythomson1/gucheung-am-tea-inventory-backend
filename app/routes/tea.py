from fastapi import APIRouter, Depends

from app.dependencies import get_teas_service
from app.services.tea_service import TeaService

router = APIRouter()


@router.get("/teas")
async def get_all_teas(service: TeaService = Depends(get_teas_service)):
    return await service.get_all()


@router.get("/teas/{tea_id}")
async def get_tea_by_id(tea_id: int, service: TeaService = Depends(get_teas_service)):
    return await service.get_by_id(tea_id)
