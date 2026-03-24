from datetime import datetime

from sqlalchemy import func, select

from app.enums import TransactionType
from app.models import StockTransaction, Tea, TeaVariant
from app.schemas import ActivityFeedResponse, CreateTransactionRequest


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    async def create(
        self,
        transaction_info: CreateTransactionRequest,
        current_user: dict,
        variant_id: int | None = None,
    ) -> StockTransaction:
        transaction = StockTransaction(
            tea_variant_id=variant_id or transaction_info.tea_variant_id,
            quantity_change=transaction_info.quantity_change,
            transaction_type=transaction_info.transaction_type,
            performed_by_id=current_user.get("sub"),
            performed_by_name=current_user.get("user_metadata", {}).get("display_name")
            or "Unknown",
            customer_id=transaction_info.customer_id,
            sales_channel=transaction_info.sales_channel,
            notes=transaction_info.notes,
        )
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def get_current_stock(self, tea_variant_id: int) -> int:
        query = select(func.sum(StockTransaction.quantity_change)).where(
            StockTransaction.tea_variant_id == tea_variant_id
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def get_latest_transactions(
        self, tea_id: int | None = None
    ) -> list[ActivityFeedResponse]:
        query = (
            select(
                StockTransaction.quantity_change,
                StockTransaction.transaction_type,
                StockTransaction.sales_channel,
                StockTransaction.customer_id,
                StockTransaction.created_at,
                StockTransaction.performed_by_name,
                StockTransaction.notes,
                TeaVariant.packaging,
                TeaVariant.flush,
                TeaVariant.harvest_year,
                TeaVariant.weight_grams,
                Tea.name.label("tea_name"),
            )
            .join(TeaVariant, TeaVariant.id == StockTransaction.tea_variant_id)
            .join(Tea, Tea.id == TeaVariant.tea_id)
            .order_by(StockTransaction.created_at.desc())
            .limit(20)
        )

        if tea_id is not None:
            query = query.where(Tea.id == tea_id)

        result = await self.db.execute(query)
        return result.mappings().all()

    async def export_transactions_as_csv(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        transaction_type: TransactionType | None = None,
        tea_name: str | None = None,
    ) -> list[ActivityFeedResponse]:
        query = (
            select(
                StockTransaction.quantity_change,
                StockTransaction.transaction_type,
                StockTransaction.sales_channel,
                StockTransaction.customer_id,
                StockTransaction.created_at,
                StockTransaction.performed_by_name,
                StockTransaction.notes,
                TeaVariant.packaging,
                TeaVariant.flush,
                TeaVariant.harvest_year,
                TeaVariant.weight_grams,
                Tea.name.label("tea_name"),
            )
            .join(TeaVariant, TeaVariant.id == StockTransaction.tea_variant_id)
            .join(Tea, Tea.id == TeaVariant.tea_id)
            .order_by(StockTransaction.created_at.desc())
        )
        if transaction_type:
            query = query.where(StockTransaction.transaction_type == transaction_type)
        if tea_name:
            query = query.where(Tea.name.ilike(f"%{tea_name}%"))
        if start_date:
            query = query.where(StockTransaction.created_at >= start_date)
        if end_date:
            query = query.where(StockTransaction.created_at <= end_date)
        result = await self.db.execute(query)
        return result.mappings().all()

    async def get_by_customer_id(self, customer_id: int) -> list[ActivityFeedResponse]:
        query = (
            select(
                StockTransaction.quantity_change,
                StockTransaction.transaction_type,
                StockTransaction.sales_channel,
                StockTransaction.customer_id,
                StockTransaction.created_at,
                StockTransaction.performed_by_name,
                StockTransaction.notes,
                TeaVariant.packaging,
                TeaVariant.flush,
                TeaVariant.harvest_year,
                TeaVariant.weight_grams,
                Tea.name.label("tea_name"),
            )
            .join(TeaVariant, TeaVariant.id == StockTransaction.tea_variant_id)
            .join(Tea, Tea.id == TeaVariant.tea_id)
            .where(StockTransaction.customer_id == customer_id)
            .order_by(StockTransaction.created_at.desc())
        )
        result = await self.db.execute(query)
        return result.mappings().all()
