from fastapi import APIRouter, Depends
from app.dependencies import get_teas_service
from app.services.teas_service import TeasService

router = APIRouter()

@router.get("/teas")
async def get_all_teas(
    service: TeasService = Depends(get_teas_service)
):
    return await service.get_all()
