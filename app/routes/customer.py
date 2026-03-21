from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.utils import get_current_user
from app.dependencies import get_customer_service, get_transaction_service
from app.schemas import (
    ActivityFeedResponse,
    CreateCustomerRequest,
    CustomerResponse,
    UpdateCustomerRequest,
)
from app.services import CustomerService, TransactionService

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


@router.patch("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    update_data: UpdateCustomerRequest,
    _: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    customer = await service.update(id=customer_id, update_data=update_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post(
    "/customers", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse
)
async def create_customer(
    customer_details: CreateCustomerRequest,
    _: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    return await service.create(customer_details=customer_details)


@router.get(
    "/customers/{customer_id}/transactions", response_model=list[ActivityFeedResponse]
)
async def get_transactions_by_customer_id(
    customer_id: int,
    _: dict = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_by_customer_id(customer_id=customer_id)
