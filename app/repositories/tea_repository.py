from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.enums import FlushType, PackagingType
from app.models import StockTransaction, Tea, TeaVariant
from app.schemas import (
    CreateTeaRequest,
    DashboardTeaResponse,
    TeaVariantStockResponse,
)


class TeaRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self) -> list[Tea]:
        query = select(Tea).where(Tea.deleted.is_(False))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Tea:
        query = select(Tea).where(Tea.id == id).options(selectinload(Tea.tea_variants))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_stock_summary(self) -> list[DashboardTeaResponse]:
        query = (
            select(
                Tea.id,
                Tea.name,
                TeaVariant.packaging,
                TeaVariant.harvest_year,
                func.sum(StockTransaction.quantity_change).label("total_stock"),
            )
            .join(TeaVariant, TeaVariant.tea_id == Tea.id)
            .join(StockTransaction, StockTransaction.tea_variant_id == TeaVariant.id)
            .group_by(Tea.id, Tea.name, TeaVariant.packaging, TeaVariant.harvest_year)
            .order_by(Tea.id, TeaVariant.packaging)
        )
        result = await self.db.execute(query)
        return result.mappings().all()

    async def get_stock_summary_by_id(
        self,
        tea_id: int,
        packaging: PackagingType | None = None,
        flush: FlushType | None = None,
        harvest_year: int | None = None,
    ) -> list[TeaVariantStockResponse]:
        query = (
            select(
                TeaVariant.id,
                TeaVariant.packaging,
                TeaVariant.flush,
                TeaVariant.harvest_year,
                TeaVariant.weight_grams,
                func.sum(StockTransaction.quantity_change).label("current_stock"),
                Tea.name.label("tea_name"),
            )
            .join(StockTransaction, StockTransaction.tea_variant_id == TeaVariant.id)
            .join(Tea, Tea.id == TeaVariant.tea_id)
            .where(TeaVariant.tea_id == tea_id)
            .group_by(TeaVariant.id, Tea.name)
        )
        if packaging:
            query = query.where(TeaVariant.packaging == packaging)
        if flush:
            query = query.where(TeaVariant.flush == flush)
        if harvest_year:
            query = query.where(TeaVariant.harvest_year == harvest_year)

        result = await self.db.execute(query)
        return result.mappings().all()

    async def create(self, tea_info: CreateTeaRequest) -> Tea:
        query = select(Tea).where(Tea.name == tea_info.name, Tea.deleted.is_(True))
        result = await self.db.execute(query)
        existing = result.scalars().first()

        if existing:
            existing.deleted = False  # type: ignore
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        tea = Tea(name=tea_info.name)
        self.db.add(tea)
        await self.db.commit()
        await self.db.refresh(tea)
        return tea

    async def soft_delete(self, id: int) -> Tea | None:
        tea = await self.get_by_id(id=id)
        if not tea:
            return None

        tea.deleted = True  # type: ignore

        await self.db.commit()
        await self.db.refresh(tea)
        return tea
