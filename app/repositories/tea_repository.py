from sqlalchemy import select
from app.models.tea import Tea

class TeaRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self):
        query = select(Tea)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id):
        query = select(Tea).where(Tea.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()
