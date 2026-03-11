from app.models import Tea, TeaVariant, StockTransaction
from app.core.database import get_db
import csv
import os
from app.core.database import SessionLocal
import uuid
import asyncio
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db = get_db()

async def seed():
    async with SessionLocal() as db:
        with open(os.path.join(BASE_DIR, 'teas.csv'), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tea = Tea(
                    id=int(row["id"]),
                    name=row["name"],
                )
                db.add(tea)

        with open(os.path.join(BASE_DIR, 'tea_variants.csv'), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tea_variant = TeaVariant(
                    id=int(row["id"]),
                    tea_id=int(row["tea_id"]),
                    packaging_type=row["packaging_type"],
                    unit=row["unit"],
                    flush=row["flush"],
                    harvest_year=int(row["harvest_year"])
                )
                db.add(tea_variant)

        with open(os.path.join(BASE_DIR, 'stock_transactions.csv'), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stock_transaction = StockTransaction(
                    id=int(row["id"]),
                    tea_variant_id=int(row["tea_variant_id"]),
                    quantity_change=int(row["quantity_change"]),
                    transaction_type=row["transaction_type"],
                    performed_by_id=uuid.UUID(row["performed_by_id"]),
                    performed_by_name=row["performed_by_name"],
                    buyer_name=row["buyer_name"] or None,
                    buyer_phone=row["buyer_phone"] or None,
                    sales_channel=row["sales_channel"] or None,
                    notes=row["notes"] or None,
                )
                db.add(stock_transaction)
        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())
