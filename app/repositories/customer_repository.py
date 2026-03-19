from sqlalchemy import select

from app.models import Customer
from app.schemas import CustomerResponse


class CustomerRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 20) -> list[CustomerResponse]:
        query = select(Customer).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
