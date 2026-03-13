from app.enums import FlushType, PackagingType
from app.models import Tea
from app.repositories import TeaRepository
from app.schemas import CreateTeaRequest, DashboardTeaResponse, TeaVariantStockResponse


class TeaService:
    def __init__(self, repository: TeaRepository):
        self.repository = repository

    async def get_all(self) -> list[Tea]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Tea | None:
        return await self.repository.get_by_id(id)

    async def get_stock_summary(self) -> list[DashboardTeaResponse]:
        return await self.repository.get_stock_summary()

    async def get_stock_summary_by_id(
        self,
        tea_id: int,
        packaging: PackagingType | None = None,
        flush: FlushType | None = None,
        harvest_year: int | None = None,
    ) -> list[TeaVariantStockResponse]:
        return await self.repository.get_stock_summary_by_id(
            tea_id, packaging, flush, harvest_year
        )

    async def add(self, tea_info: CreateTeaRequest) -> Tea:
        return await self.repository.add(tea_info=tea_info)
