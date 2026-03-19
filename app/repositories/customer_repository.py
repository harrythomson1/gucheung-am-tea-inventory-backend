from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Customer


class CustomerRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(
        self, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> list[Customer]:
        query = select(Customer)
        if search:
            query = query.where(
                Customer.name.ilike(f"%{search}%")
                | Customer.city.ilike(f"%{search}%")
                | Customer.phone.ilike(f"%{search}%")
            )
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Customer | None:
        query = (
            select(Customer)
            .where(Customer.id == id)
            .options(selectinload(Customer.stock_transactions))
        )
        result = await self.db.execute(query)
        return result.scalars().first()
