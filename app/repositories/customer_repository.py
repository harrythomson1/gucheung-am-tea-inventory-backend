from sqlalchemy import select

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
