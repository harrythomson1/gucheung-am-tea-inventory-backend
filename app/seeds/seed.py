import asyncio
import csv
import os
import uuid

from app.core.database import SessionLocal, get_db
from app.models import Customer, StockTransaction, Tea, TeaVariant

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db = get_db()


async def seed():
    async with SessionLocal() as db:
        with open(os.path.join(BASE_DIR, "teas.csv"), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tea = Tea(
                    id=int(row["id"]),
                    name=row["name"],
                )
                db.add(tea)

        with open(os.path.join(BASE_DIR, "tea_variants.csv"), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tea_variant = TeaVariant(
                    id=int(row["id"]),
                    tea_id=int(row["tea_id"]),
                    packaging=row["packaging"],
                    weight_grams=int(row["weight_grams"]),
                    flush=row["flush"],
                    harvest_year=int(row["harvest_year"]),
                )
                db.add(tea_variant)

        with open(os.path.join(BASE_DIR, "customers.csv"), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                customer = Customer(
                    id=int(row["id"]),
                    name=row["name"],
                    city=row["city"],
                    address=row["address"] or None,
                    phone=row["phone"] or None,
                    notes=row["notes"] or None,
                )
                db.add(customer)

        with open(
            os.path.join(BASE_DIR, "stock_transactions.csv"), newline=""
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stock_transaction = StockTransaction(
                    id=int(row["id"]),
                    tea_variant_id=int(row["tea_variant_id"]),
                    quantity_change=int(row["quantity_change"]),
                    transaction_type=row["transaction_type"],
                    performed_by_id=uuid.UUID(row["performed_by_id"]),
                    performed_by_name=row["performed_by_name"],
                    customer_id=int(row["customer_id"]) if row["customer_id"] else None,
                    sales_channel=row["sales_channel"] or None,
                    notes=row["notes"] or None,
                )
                db.add(stock_transaction)
        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
