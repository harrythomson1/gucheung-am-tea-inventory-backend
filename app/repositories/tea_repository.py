from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.tea import Tea


class TeaRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self) -> list[Tea]:
        query = select(Tea)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Tea:
        query = select(Tea).where(Tea.id == id).options(selectinload(Tea.tea_variants))
        result = await self.db.execute(query)
        return result.scalars().first()
