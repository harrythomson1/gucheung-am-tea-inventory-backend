from sqlalchemy import select

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 20):
        query = select(Customer).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
