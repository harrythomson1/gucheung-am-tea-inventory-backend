from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.utils import get_current_user, require_admin
from app.dependencies import get_teas_service
from app.enums import FlushType, PackagingType
from app.schemas import (
    CreateTeaRequest,
    TeaDetailResponse,
    TeaResponse,
    TeaVariantStockResponse,
)
from app.services import TeaService

router = APIRouter()


@router.get("/teas", response_model=list[TeaResponse])
async def get_all_teas(
    _: dict = Depends(get_current_user), service: TeaService = Depends(get_teas_service)
):
    return await service.get_all()


@router.get("/teas/{tea_id}", response_model=TeaDetailResponse)
async def get_tea_by_id(
    tea_id: int,
    _: dict = Depends(get_current_user),
    service: TeaService = Depends(get_teas_service),
):
    tea = await service.get_by_id(tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea


@router.get("/teas/{tea_id}/stock", response_model=list[TeaVariantStockResponse])
async def get_stock_summary_by_id(
    tea_id: int,
    _: dict = Depends(get_current_user),
    packaging: PackagingType | None = None,
    flush: FlushType | None = None,
    harvest_year: int | None = None,
    service: TeaService = Depends(get_teas_service),
):
    stock_summary = await service.get_stock_summary_by_id(
        tea_id, packaging, flush, harvest_year
    )
    if not stock_summary:
        raise HTTPException(status_code=404, detail="Stock summary not found")
    return stock_summary


@router.post("/teas", status_code=status.HTTP_201_CREATED)
async def create_tea(
    tea_info: CreateTeaRequest,
    _: dict = Depends(require_admin),
    service: TeaService = Depends(get_teas_service),
):
    try:
        return await service.create(tea_info=tea_info)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


@router.delete("/teas/{tea_id}", status_code=204)
async def soft_delete(
    tea_id: int,
    _: dict = Depends(get_current_user),
    service: TeaService = Depends(get_teas_service),
):
    tea = await service.soft_delete(id=tea_id)
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return None
