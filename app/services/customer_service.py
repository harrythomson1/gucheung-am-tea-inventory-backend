from app.models import Customer
from app.repositories import CustomerRepository


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def get_all(
        self, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> list[Customer]:
        return await self.repository.get_all(skip=skip, limit=limit, search=search)
