import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import FlushType, PackagingType, TransactionType
from app.models import Tea, TeaVariant
from app.schemas import CreateTransactionRequest
from app.services import TransactionService


@pytest_asyncio.fixture
async def tea_variant(db_session: AsyncSession):
    tea = Tea(name="청차")
    db_session.add(tea)
    await db_session.commit()
    await db_session.refresh(tea)

    variant = TeaVariant(
        tea_id=tea.id,
        packaging=PackagingType.silver,
        flush=FlushType.first,
        harvest_year=2024,
        weight_grams=40,
    )
    db_session.add(variant)
    await db_session.commit()
    await db_session.refresh(variant)
    return variant


async def test_removal_raises_400_when_insufficient_stock(
    service: TransactionService,
    tea_variant: TeaVariant,
):
    request = CreateTransactionRequest(
        tea_variant_id=tea_variant.id,  # type: ignore
        quantity_change=-10,
        transaction_type=TransactionType.sale,
    )

    with pytest.raises(HTTPException) as exc_info:
        await service._create_removal(
            transaction_info=request,
            current_user={
                "sub": "test-user",
                "user_metadata": {"display_name": "Test"},
            },
        )

    assert exc_info.value.status_code == 400
    assert "stock" in exc_info.value.detail.lower()
