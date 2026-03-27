from sqlalchemy import select

from app.models import Customer
from app.schemas import CreateCustomerRequest, UpdateCustomerRequest


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
        query = query.order_by(Customer.updated_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Customer | None:
        query = select(Customer).where(Customer.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update(
        self, id: int, update_data: UpdateCustomerRequest
    ) -> Customer | None:
        customer = await self.get_by_id(id)
        if not customer:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(customer, key, value)

        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def create(self, customer_details: CreateCustomerRequest) -> Customer:
        customer = Customer(
            name=customer_details.name,
            city=customer_details.city,
            address_1=customer_details.address_1,
            address_2=customer_details.address_2,
            postcode=customer_details.postcode,
            phone=customer_details.phone,
            notes=customer_details.notes,
        )
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
