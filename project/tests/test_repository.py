from decimal import Decimal

import pytest
from sqlalchemy import text

from app import models, repository


@pytest.mark.asyncio
async def test_repository_can_save_a_loan(session):
    borrower = models.Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    await borrower_repo.add(borrower)
    await session.commit()

    borrower_rows = list(
        await session.execute(
            text(
                """
            SELECT * FROM borrowers
            """
            )
        )
    )
    assert borrower_rows == [(borrower.id, "John Doe", "john@example.com", 700)]

    loan = models.Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
    )
    repo = repository.SqlAlchemyLoanRepository(session)
    await repo.add(loan)
    await session.commit()

    rows = list(
        await session.execute(
            text("SELECT borrower_id, amount, purpose, term_months FROM loans")
        )
    )

    borrower_id, amount, purpose, term_months = rows[0]

    assert str(loan.borrower.id) == str(borrower_id)
    assert loan.amount == Decimal(amount)
    assert loan.purpose == purpose
    assert loan.term_months == term_months


@pytest.mark.asyncio
async def test_repository_can_save_an_investment(session):
    # Create an investor and commit
    investor = models.Investor(
        name="Warren Buffet",
        email="warren@example.com",
        available_funds=Decimal("1500"),
    )
    investor_repo = repository.SqlAlchemyInvestorRepository(session)
    await investor_repo.add(investor)
    await session.commit()

    investor_from_db = await investor_repo.get(investor_id=investor.id)
    assert investor_from_db is not None
    await session.commit()

    assert investor_from_db.id == investor.id

    # Create a Borrower and commit
    borrower = models.Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    await borrower_repo.add(borrower)
    await session.commit()
    borrower_from_db = await borrower_repo.get(borrower_id=borrower.id)
    await session.commit()
    assert borrower_from_db == borrower

    # Create a Loan, assign the borrow to it and commit
    loan = models.Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
    )
    repo_loan = repository.SqlAlchemyLoanRepository(session)
    await repo_loan.add(loan)
    await session.commit()
    loan_from_db = await repo_loan.get(loan_id=loan.id)
    assert loan_from_db is not None
    assert loan_from_db.borrower.id == borrower.id
    assert loan_from_db.purpose == loan.purpose
    assert loan_from_db.amount == loan.amount

    # Create an Investment, assign the investor and loan to it and commit
    investment = models.Investment(investor=investor, loan=loan, amount=loan.amount)
    investment_repo = repository.SqlAlchemyInvestmentRepository(session)
    await investment_repo.add(investment)
    await session.commit()
    # Verify the investment is saved correctly

    investment_from_db = await investment_repo.get(investment_id=investment.id)
    if investment_from_db is None:
        raise ValueError("Investment not found")
    assert investment_from_db.investor.id == investor.id
    assert investment_from_db.loan.id == loan.id
    assert investment_from_db.amount == investment.amount
    assert investment_from_db.status == investment.status
