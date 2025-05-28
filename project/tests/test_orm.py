import logging
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import text

from app.models import (
    Borrower,
    Investment,
    InvestmentStatus,
    Investor,
    Loan,
    LoanStatus,
)


logger = logging.getLogger(__name__)


def test_borrower_mapper_can_save_borrower(session):
    # Using raw SQL
    borrower_id = str(uuid4())
    session.execute(
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
    session.commit()

    # Using ORM
    saved_borrower = session.query(Borrower).first()
    assert saved_borrower.name == "John Doe"
    assert saved_borrower.email == "john@example.com"
    assert saved_borrower.credit_score == 700


def test_loan_mapper_can_save_loan(session):
    borrower = Borrower(
        name="John Doe",
        email="john@example.com",
        credit_score=700,
    )
    session.add(borrower)
    session.commit()

    loan = Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
        # id=loan_id
    )
    session.add(loan)
    session.commit()

    # Verify using raw SQL
    rows = list(
        session.execute(text("SELECT amount, purpose, term_months, status FROM loans"))
    )
    amount, purpose, term_months, status = rows[0]
    assert amount == Decimal("1000.00")
    assert purpose == "Home improvement"
    assert term_months == 12
    assert status == "ACTIVE"

    # Verify using ORM
    saved_loan = session.query(Loan).first()
    assert saved_loan.amount == Decimal("1000.00")
    assert saved_loan.purpose == "Home improvement"
    assert saved_loan.term_months == 12
    assert saved_loan.status == LoanStatus.ACTIVE
    assert saved_loan.borrower.name == "John Doe"


def test_investment_mapper_can_save_investment(session):
    borrower = Borrower(name="John Doe", email="john@example.com", credit_score=700)
    session.add(borrower)

    loan = Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
    )
    session.add(loan)

    investor = Investor(
        name="Jane Smith", email="jane@example.com", available_funds=Decimal("5000.00")
    )
    session.add(investor)
    session.commit()

    investment = Investment(investor=investor, loan=loan, amount=Decimal("500.00"))
    session.add(investment)
    session.commit()

    saved_investment = session.query(Investment).first()
    assert saved_investment.amount == Decimal("500.00")
    assert saved_investment.status == InvestmentStatus.PENDING_APPROVAL
    assert saved_investment.investor.name == "Jane Smith"
    assert saved_investment.loan.purpose == "Home improvement"
