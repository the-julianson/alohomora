from decimal import Decimal

import pytest

from app.models import (
    Borrower,
    InvalidInvestmentAmountError,
    Investment,
    InvestmentStatus,
    Investor,
    Loan,
    LoanAlreadyFundedError,
    LoanStatus,
    Repayment,
)


def test_borrower_can_create_loan_with_good_credit():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    assert borrower.can_create_loan() is True


def test_borrower_cannot_create_loan_with_bad_credit():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=500
    )
    assert borrower.can_create_loan() is False


def test_investor_can_invest_with_sufficient_funds():
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )
    assert investor.can_invest(Decimal("5000.00")) is True


def test_investor_cannot_invest_with_insufficient_funds():
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("1000.00"),
    )
    assert investor.can_invest(Decimal("5000.00")) is False


def test_investor_funds_are_reduced_when_investing():
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )
    investor.invest(Decimal("5000.00"))
    assert investor.available_funds == Decimal("5000.00")


def test_investor_funds_are_increased_when_refunded():
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("5000.00"),
    )
    investor.refund(Decimal("1000.00"))
    assert investor.available_funds == Decimal("6000.00")


def test_loan_can_accept_investment():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    assert loan.can_accept_investment(Decimal("5000.00")) is True


def test_loan_cannot_accept_investment_with_different_amount():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    assert loan.can_accept_investment(Decimal("3000.00")) is False


def test_loan_cannot_accept_investment_when_already_funded():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )
    investment = Investment(
        investor=investor, loan=loan, amount=Decimal("5000.00")
    )
    loan.accept_investment(investment)

    with pytest.raises(LoanAlreadyFundedError):
        loan.accept_investment(investment)


def test_investment_validation():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )
    investment = Investment(
        investor=investor, loan=loan, amount=Decimal("3000.00")
    )

    with pytest.raises(InvalidInvestmentAmountError):
        investment.validate_amount()


def test_investment_approval():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )
    investment = Investment(
        investor=investor, loan=loan, amount=Decimal("5000.00")
    )

    investment.approve()

    assert investment.status == InvestmentStatus.ACTIVE
    assert loan.status == LoanStatus.FUNDED
    assert loan.investment == investment


def test_investment_rejection():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )

    # First withdraw the funds
    investor.invest(Decimal("5000.00"))
    assert investor.available_funds == Decimal("5000.00")

    # Then create the investment
    investment = Investment(
        investor=investor, loan=loan, amount=Decimal("5000.00")
    )

    investment.reject()

    assert investment.status == InvestmentStatus.REJECTED
    assert loan.status == LoanStatus.ACTIVE
    assert loan.investment is None
    assert investor.available_funds == Decimal("10000.00")


def test_repayment_validation():
    borrower = Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    loan = Loan(
        borrower=borrower,
        amount=Decimal("5000.00"),
        purpose="Business expansion",
        term_months=12,
    )
    investor = Investor(
        name="Jane Smith",
        email="jane@example.com",
        available_funds=Decimal("10000.00"),
    )
    investment = Investment(
        investor=investor, loan=loan, amount=Decimal("5000.00")
    )

    with pytest.raises(
        ValueError,
        match="Repayment amount exceeds remaining investment amount",
    ):
        Repayment(
            investment=investment, amount=Decimal("6000.00")
        ).validate_amount()
