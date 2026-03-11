from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_teas_service
from app.schemas.tea import TeaDetailResponse, TeaResponse
from app.services.tea_service import TeaService

router = APIRouter()


@router.get("/teas", response_model=list[TeaResponse])
async def get_all_teas(service: TeaService = Depends(get_teas_service)):
    teas = await service.get_all()
    if not teas:
        raise HTTPException(status_code=404, detail="No teas found")
    return teas


@router.get("/teas/{tea_id}", response_model=TeaDetailResponse)
async def get_tea_by_id(tea_id: int, service: TeaService = Depends(get_teas_service)):
    tea = await service.get_by_id(tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea
