from fastapi import APIRouter, Depends, HTTPException

from app.auth.utils import get_current_user
from app.dependencies import get_customer_service
from app.schemas import CustomerResponse
from app.services import CustomerService

router = APIRouter()


@router.get("/customers", response_model=list[CustomerResponse])
async def get_all(
    _: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
):
    customers = await service.get_all(skip=skip, limit=limit, search=search)
    return customers


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_by_id(
    customer_id: int,
    _: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    customer = await service.get_by_id(id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
