from sqlalchemy import select

from app.models import TeaVariant
from app.schemas.transaction import CreateTransactionRequest


class TeaVariantRepository:
    def __init__(self, db):
        self.db = db

    async def find_or_create(
        self, variant_info: CreateTransactionRequest
    ) -> TeaVariant:
        query = select(TeaVariant).where(
            TeaVariant.tea_id == variant_info.tea_id,
            TeaVariant.packaging == variant_info.packaging,
            TeaVariant.flush == variant_info.flush,
            TeaVariant.harvest_year == variant_info.harvest_year,
            TeaVariant.weight_grams == variant_info.weight_grams,
        )
        result = await self.db.execute(query)
        variant = result.scalars().first()

        if variant:
            return variant

        variant = TeaVariant(
            tea_id=variant_info.tea_id,
            packaging=variant_info.packaging,
            flush=variant_info.flush,
            harvest_year=variant_info.harvest_year,
            weight_grams=variant_info.weight_grams,
        )
        self.db.add(variant)
        await self.db.commit()
        await self.db.refresh(variant)
        return variant

    async def get_by_id(self, tea_variant_id: int) -> TeaVariant | None:
        query = select(TeaVariant).where(TeaVariant.id == tea_variant_id)
        result = await self.db.execute(query)
        return result.scalars().first()
