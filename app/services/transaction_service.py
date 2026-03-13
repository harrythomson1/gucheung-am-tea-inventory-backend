from datetime import datetime

from fastapi import HTTPException

from app.enums import TransactionType
from app.models import StockTransaction
from app.repositories import TeaRepository, TeaVariantRepository, TransactionRepository
from app.schemas import ActivityFeedResponse, CreateTransactionRequest


class TransactionService:
    def __init__(
        self,
        repository: TransactionRepository,
        tea_repository: TeaRepository,
        tea_variant_repository: TeaVariantRepository,
    ):
        self.repository = repository
        self.tea_repository = tea_repository
        self.tea_variant_repository = tea_variant_repository

    async def create(
        self, transaction_info: CreateTransactionRequest
    ) -> StockTransaction:
        if transaction_info.transaction_type == TransactionType.harvest:
            return await self._create_harvest(transaction_info)
        else:
            return await self._create_removal(transaction_info)

    async def get_latest_transactions(self) -> list[ActivityFeedResponse]:
        return await self.repository.get_latest_transactions()

    async def export_transactions_as_csv(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        transaction_type: TransactionType | None = None,
        tea_name: str | None = None,
        buyer_name: str | None = None,
    ) -> list[ActivityFeedResponse]:
        return await self.repository.export_transactions_as_csv(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type,
            tea_name=tea_name,
            buyer_name=buyer_name,
        )

    async def _create_harvest(
        self, transaction_info: CreateTransactionRequest
    ) -> StockTransaction:
        tea = await self.tea_repository.get_by_id(int(transaction_info.tea_id))  # type: ignore
        if not tea:
            raise HTTPException(status_code=404, detail="Tea not found")
        variant = await self.tea_variant_repository.find_or_create(transaction_info)
        transaction = await self.repository.create(transaction_info, int(variant.id))  # type: ignore
        return transaction

    async def _create_removal(
        self, transaction_info: CreateTransactionRequest
    ) -> StockTransaction:
        variant = await self.tea_variant_repository.get_by_id(
            int(transaction_info.tea_variant_id)  # type: ignore
        )
        if not variant:
            raise HTTPException(status_code=404, detail="variant not found")
        current_stock = await self.repository.get_current_stock(int(variant.id))  # type: ignore
        if current_stock + transaction_info.quantity_change < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        return await self.repository.create(transaction_info, int(variant.id))  # type: ignore
