import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.auth.utils import get_current_user, require_admin
from app.dependencies import get_transaction_service
from app.enums import TransactionType
from app.schemas import ActivityFeedResponse, CreateTransactionRequest
from app.services import TransactionService

router = APIRouter()

transaction_service_dependency = Depends(get_transaction_service)


@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_info: CreateTransactionRequest,
    current_user: dict = Depends(get_current_user),
    service: TransactionService = transaction_service_dependency,
):
    return await service.create(transaction_info, current_user)


@router.get("/transactions", response_model=list[ActivityFeedResponse])
async def get_latest_transactions(
    _: dict = Depends(require_admin),
    service: TransactionService = Depends(get_transaction_service),
    tea_id: int | None = None,
):
    return await service.get_latest_transactions(tea_id=tea_id)


@router.get("/transactions/export")
async def export_transactions_as_csv(
    _: dict = Depends(get_current_user),
    service: TransactionService = transaction_service_dependency,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    transaction_type: TransactionType | None = None,
    tea_name: str | None = None,
):
    transactions = await service.export_transactions_as_csv(
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        tea_name=tea_name,
    )

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "quantity_change",
            "transaction_type",
            "sales_channel",
            "customer_id",
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
    writer.writerows(
        [
            {k: v.value if hasattr(v, "value") else v for k, v in dict(t).items()}
            for t in transactions
        ]
    )

    return StreamingResponse(
        io.StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )
