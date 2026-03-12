from app.models import Tea
from app.repositories import TeaRepository
from app.schemas import DashboardTeaResponse


class TeaService:
    def __init__(self, repository: TeaRepository):
        self.repository = repository

    async def get_all(self) -> list[Tea]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Tea | None:
        return await self.repository.get_by_id(id)

    async def get_stock_summary(self) -> list[DashboardTeaResponse]:
        return await self.repository.get_stock_summary()
