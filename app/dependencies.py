from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import (
    CustomerRepository,
    TeaRepository,
    TeaVariantRepository,
    TransactionRepository,
)
from app.services import CustomerService, TeaService, TransactionService


async def get_tea_repository(db: AsyncSession = Depends(get_db)):
    return TeaRepository(db)


async def get_transaction_repository(db: AsyncSession = Depends(get_db)):
    return TransactionRepository(db)


async def get_tea_variant_repository(db: AsyncSession = Depends(get_db)):
    return TeaVariantRepository(db)


async def get_customer_repository(db: AsyncSession = Depends(get_db)):
    return CustomerRepository(db)


async def get_teas_service(
    tea_repository=Depends(get_tea_repository),
):
    return TeaService(repository=tea_repository)


async def get_transaction_service(
    transaction_repository=Depends(get_transaction_repository),
    tea_repository=Depends(get_tea_repository),
    tea_variant_repository=Depends(get_tea_variant_repository),
):
    return TransactionService(
        repository=transaction_repository,
        tea_repository=tea_repository,
        tea_variant_repository=tea_variant_repository,
    )


async def get_customer_service(customer_repository=Depends(get_customer_repository)):
    return CustomerService(repository=customer_repository)
