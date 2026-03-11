from fastapi import APIRouter, Depends, status

from app.dependencies import get_transaction_service
from app.schemas.transaction import CreateTransactionRequest
from app.services.transaction_service import TransactionService

router = APIRouter()

transaction_service_dependency = Depends(get_transaction_service)


@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_info: CreateTransactionRequest,
    service: TransactionService = transaction_service_dependency,
):
    await service.create(transaction_info)
    return None
