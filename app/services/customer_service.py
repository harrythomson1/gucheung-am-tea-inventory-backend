from app.models import Customer
from app.repositories import CustomerRepository
from app.schemas import UpdateCustomerRequest


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def get_all(
        self, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> list[Customer]:
        return await self.repository.get_all(skip=skip, limit=limit, search=search)

    async def get_by_id(self, id: int) -> Customer | None:
        return await self.repository.get_by_id(id)

    async def update(
        self, id: int, update_data: UpdateCustomerRequest
    ) -> Customer | None:
        return await self.repository.update(id=id, update_data=update_data)
