import logging
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.models import (
    Borrower,
    Investment,
    InvestmentStatus,
    Investor,
    Loan,
    LoanStatus,
)


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_borrower_mapper_can_save_borrower(session):
    # Using raw SQL
    borrower_id = str(uuid4())
    await session.execute(
        text(
            """INSERT INTO borrowers
            (id, name, email, credit_score)
            VALUES (:id, :name, :email, :credit_score)"""
        ),
        {
            "id": borrower_id,
            "name": "John Doe",
            "email": "john@example.com",
            "credit_score": 700,
        },
    )
    await session.commit()

    # Using ORM with modern async syntax
    stmt = select(Borrower)
    result = await session.execute(stmt)
    saved_borrower = result.scalar_one_or_none()
    assert saved_borrower.name == "John Doe"
    assert saved_borrower.email == "john@example.com"
    assert saved_borrower.credit_score == 700


@pytest.mark.asyncio
async def test_loan_mapper_can_save_loan(session):
    borrower = Borrower(
        name="John Doe",
        email="john@example.com",
        credit_score=700,
    )
    session.add(borrower)
    await session.commit()

    loan = Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
        # id=loan_id
    )
    session.add(loan)
    await session.commit()

    # Verify using raw SQL
    rows = await session.execute(
        text("SELECT amount, purpose, term_months, status FROM loans")
    )

    amount, purpose, term_months, status = rows.first()
    assert amount == Decimal("1000.00")
    assert purpose == "Home improvement"
    assert term_months == 12
    assert status == "ACTIVE"

    # Verify using ORM with modern async syntax
    result = await session.execute(select(Loan))  # <- select the Loan class
    saved_loan = result.scalar_one_or_none()
    assert saved_loan.amount == Decimal("1000.00")
    assert saved_loan.purpose == "Home improvement"
    assert saved_loan.term_months == 12
    assert saved_loan.status == LoanStatus.ACTIVE
    assert saved_loan.borrower.name == "John Doe"


@pytest.mark.asyncio
async def test_investment_mapper_can_save_investment(session):
    borrower = Borrower(name="John Doe", email="john@example.com", credit_score=700)
    session.add(borrower)
    await session.commit()

    loan = Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
    )
    session.add(loan)
    await session.commit()

    investor = Investor(
        name="Jane Smith", email="jane@example.com", available_funds=Decimal("5000.00")
    )
    session.add(investor)
    await session.commit()

    investment = Investment(investor=investor, loan=loan, amount=Decimal("500.00"))
    session.add(investment)
    await session.commit()

    # Using modern async syntax
    result = await session.execute(select(Investment))
    saved_investment = result.scalar_one_or_none()
    assert saved_investment.amount == Decimal("500.00")
    assert saved_investment.status == InvestmentStatus.PENDING_APPROVAL
    assert saved_investment.investor.name == "Jane Smith"
    assert saved_investment.loan.purpose == "Home improvement"
