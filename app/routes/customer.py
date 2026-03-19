from fastapi import APIRouter, Depends

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
