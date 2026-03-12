from fastapi import HTTPException


class TransactionService:
    def __init__(self, repository, tea_repository, transaction_repository):
        self.repository = repository
        self.tea_repository = tea_repository
        self.transaction_repository = transaction_repository

    async def _create_harvest(self, transaction_info):
        tea = self.tea_repository.get_by_id(transaction_info.tea_id)
        if not tea:
            raise HTTPException(status_code=404, detail="Tea not found")
