from fastapi import HTTPException

from app.enums import TransactionType
from app.models import StockTransaction
from app.repositories import TeaRepository, TeaVariantRepository, TransactionRepository
from app.schemas import CreateTransactionRequest


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
