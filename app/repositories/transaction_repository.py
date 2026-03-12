from app.models import StockTransaction


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, transaction_info, variant_id=None):
        transaction = StockTransaction(
            tea_variant_id=variant_id or transaction_info.tea_variant_id,
            quantity_change=transaction_info.quantity_change,
            transaction_type=transaction_info.transaction_type,
            performed_by_id=transaction_info.performed_by_id,
            performed_by_name=transaction_info.performed_by_name,
            buyer_name=transaction_info.buyer_name,
            buyer_phone=transaction_info.buyer_phone,
            sales_channel=transaction_info.sales_channel,
            notes=transaction_info.notes,
        )
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction
