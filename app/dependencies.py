from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.tea_repository import TeaRepository
from app.repositories.tea_variant_repository import TeaVariantRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.tea_service import TeaService
from app.services.transaction_service import TransactionService


async def get_tea_repository(db: AsyncSession = Depends(get_db)):
    return TeaRepository(db)


async def get_transaction_repository(db: AsyncSession = Depends(get_db)):
    return TransactionRepository(db)


async def get_tea_variant_repository(db: AsyncSession = Depends(get_db)):
    return TeaVariantRepository(db)


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
