from fastapi import HTTPException

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

    async def _create_harvest(
        self, transaction_info: CreateTransactionRequest
    ) -> StockTransaction:
        tea = await self.tea_repository.get_by_id(transaction_info.tea_id)
        if not tea:
            raise HTTPException(status_code=404, detail="Tea not found")
        variant = await self.tea_variant_repository.find_or_create(transaction_info)
        transaction = await self.repository.create(transaction_info, int(variant.id))  # type: ignore
        return transaction
