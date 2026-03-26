import pytest
import pytest_asyncio
from fastapi import HTTPException
from pydantic_core import ValidationError
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


async def test_removal_lowers_current_stock_on_tea_variant(
    service: TransactionService,
    tea_variant: TeaVariant,
    db_session: AsyncSession,
):
    harvest_request = CreateTransactionRequest(
        tea_variant_id=tea_variant.id,  # type: ignore
        quantity_change=10,
        transaction_type=TransactionType.harvest,
        tea_id=tea_variant.tea_id,  # type: ignore
        packaging=PackagingType.silver,
        flush=FlushType.first,
        harvest_year=2024,
        weight_grams=40,
    )
    await service._create_harvest(
        transaction_info=harvest_request,
        current_user={
            "sub": "00000000-0000-0000-0000-000000000001",
            "user_metadata": {"display_name": "Test"},
        },
    )

    removal_request = CreateTransactionRequest(
        tea_variant_id=tea_variant.id,  # type: ignore
        quantity_change=-5,
        transaction_type=TransactionType.sale,
    )
    await service._create_removal(
        transaction_info=removal_request,
        current_user={
            "sub": "00000000-0000-0000-0000-000000000001",
            "user_metadata": {"display_name": "Test"},
        },
    )

    from app.repositories import TransactionRepository

    repo = TransactionRepository(db_session)
    current_stock = await repo.get_current_stock(tea_variant.id)  # type: ignore
    assert current_stock == 5


def test_removal_raises_validation_error_when_value_is_positive():
    with pytest.raises(ValidationError) as e:
        CreateTransactionRequest(
            tea_variant_id=1,
            quantity_change=5,
            transaction_type=TransactionType.sale,
        )
    assert (
        e.value.errors()[0]["msg"]
        == "Value error, quantity_change must be negative for non-harvest transactions"
    )


def test_harvest_raises_validation_error_when_value_is_negative():
    with pytest.raises(ValidationError) as e:
        CreateTransactionRequest(
            tea_variant_id=1,
            quantity_change=-5,
            transaction_type=TransactionType.harvest,
            tea_id=1,
            packaging=PackagingType.silver,
            flush=FlushType.first,
            harvest_year=2024,
            weight_grams=40,
        )

    assert (
        e.value.errors()[0]["msg"]
        == "Value error, quantity_change must be positive for harvest transactions"
    )


async def test_harvest_raises_current_stock_on_tea_variant(
    service: TransactionService,
    tea_variant: TeaVariant,
    db_session: AsyncSession,
):
    harvest_request = CreateTransactionRequest(
        tea_variant_id=tea_variant.id,  # type: ignore
        quantity_change=10,
        transaction_type=TransactionType.harvest,
        tea_id=tea_variant.tea_id,  # type: ignore
        packaging=PackagingType.silver,
        flush=FlushType.first,
        harvest_year=2024,
        weight_grams=40,
    )
    await service._create_harvest(
        transaction_info=harvest_request,
        current_user={
            "sub": "00000000-0000-0000-0000-000000000001",
            "user_metadata": {"display_name": "Test"},
        },
    )

    from app.repositories import TransactionRepository

    repo = TransactionRepository(db_session)
    current_stock = await repo.get_current_stock(tea_variant.id)  # type: ignore
    assert current_stock == 10
