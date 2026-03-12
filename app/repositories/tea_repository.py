from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models import StockTransaction, Tea, TeaVariant
from app.schemas import DashboardTeaResponse


class TeaRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self) -> list[Tea]:
        query = select(Tea)
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
                func.sum(StockTransaction.quantity_change).label("total_stock"),
            )
            .join(TeaVariant, TeaVariant.tea_id == Tea.id)
            .join(StockTransaction, StockTransaction.tea_variant_id == TeaVariant.id)
            .group_by(Tea.id, Tea.name)
        )
        result = await self.db.execute(query)
        return result.mappings().all()
