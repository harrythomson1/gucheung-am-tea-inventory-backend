import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.dependencies import get_transaction_service
from app.enums import TransactionType
from app.schemas import ActivityFeedResponse, CreateTransactionRequest
from app.services.transaction_service import TransactionService

router = APIRouter()

transaction_service_dependency = Depends(get_transaction_service)


@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_info: CreateTransactionRequest,
    service: TransactionService = transaction_service_dependency,
):
    await service.create(transaction_info)
    return None


@router.get("/transactions", response_model=list[ActivityFeedResponse])
async def get_latest_transactions(
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_latest_transactions()


@router.get("/transactions/export")
async def export_transactions_as_csv(
    service: TransactionService = transaction_service_dependency,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    transaction_type: TransactionType | None = None,
    tea_name: str | None = None,
    buyer_name: str | None = None,
):
    transactions = await service.export_transactions_as_csv(
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        tea_name=tea_name,
        buyer_name=buyer_name,
    )

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "quantity_change",
            "transaction_type",
            "sales_channel",
            "buyer_name",
            "created_at",
            "performed_by_name",
            "notes",
            "packaging",
            "flush",
            "harvest_year",
            "weight_grams",
            "tea_name",
        ],
    )
    writer.writeheader()
    writer.writerows([dict(t) for t in transactions])

    return StreamingResponse(
        io.StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )
