from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.tea_service import TeaService
from app.repositories.tea_repository import TeaRepository
from app.core.database import get_db


async def get_tea_repository(db: AsyncSession = Depends(get_db)):
    return TeaRepository(db)

async def get_teas_service(
    tea_repository=Depends(get_tea_repository),
):
    return TeaService(
        repository=tea_repository
    )
