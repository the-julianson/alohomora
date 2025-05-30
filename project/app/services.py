# app/services.py

import logging

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.helper import calculate_credit_score
from app.models import Borrower, InsufficientCreditScoreError, Loan, LoanStatus
from app.repository import (
    SqlAlchemyBorrowerRepository,
    SqlAlchemyInvestorRepository,
    SqlAlchemyLoanRepository,
)


logger = logging.getLogger(__name__)


class BorrowerDTO(BaseModel):
    id: str
    name: str
    email: str
    credit_score: int


class CreateBorrowerDTO(BaseModel):
    name: str
    email: str
    income: int
    employment_years: int
    has_previous_loans: bool


class LoanApplicationDTO(BaseModel):
    borrower_id: str
    amount: int
    term_months: int
    purpose: str


class InvestorCreateDTO(BaseModel):
    name: str
    email: str
    available_funds: int


class LoanApplicationError(Exception):
    pass


async def create_borrower(
    prospect_borrower: CreateBorrowerDTO,
    borrower_repo: SqlAlchemyBorrowerRepository,
    session: AsyncSession,
) -> tuple[str, int]:
    """
    Create a new borrower with calculated credit score.
    Returns tuple of (borrower_id, credit_score)
    """
    logger.info("Starting borrower creation")
    credit_score = calculate_credit_score(
        income=prospect_borrower.income,
        employment_years=prospect_borrower.employment_years,
        has_previous_loans=prospect_borrower.has_previous_loans,
    )

    borrower = Borrower(
        name=prospect_borrower.name,
        email=prospect_borrower.email,
        credit_score=credit_score,
    )
    await borrower_repo.add(borrower)
    await session.commit()
    return str(borrower.id), credit_score


async def apply_for_loan(
    loan_object: Loan, loan_repo: SqlAlchemyLoanRepository, session: AsyncSession
) -> str:
    """
    Apply for a new loan with the following rules:
    - If borrower has 2 or more FUNDED or REPAYING loans, reject
    - If borrower has any DEFAULTED loans, reject
    - If borrower has 2 ACTIVE loans, allow up to 4 ACTIVE loans
    - Otherwise, allow the loan
    """
    # Get all loan counts in a single query
    # CHECK SCORING OF BORROWER
    if not loan_object.borrower.can_create_loan():
        raise InsufficientCreditScoreError("""Borrower has insufficient credit score
        (minimum 600 required)""")

    # Get all loan counts for the borrower
    loan_counts = await loan_repo.get_loan_counts_by_status(loan_object.borrower.id)

    # Check for defaulted loans
    if loan_counts.get(LoanStatus.DEFAULTED, 0) > 0:
        raise LoanApplicationError("""Cannot apply for loan:
        Borrower has defaulted loans""")

    # Check for funded/repaying loans
    active_loans = loan_counts.get(LoanStatus.FUNDED, 0) + loan_counts.get(
        LoanStatus.REPAYING, 0
    )
    if active_loans >= 2:
        raise LoanApplicationError("""Cannot apply for loan:
         Borrower has maximum allowed active loans""")

    # Check for pending loans
    pending_loans = loan_counts.get(LoanStatus.ACTIVE, 0)
    if pending_loans >= 4:
        raise LoanApplicationError("""Cannot apply for loan:
        Borrower has maximum allowed pending approval loans""")

    # If we get here, the loan is allowed
    await loan_repo.add(loan_object)
    await session.commit()
    return loan_object.id


async def get_borrowers(
    borrower_repo: SqlAlchemyBorrowerRepository, session: AsyncSession
) -> list[Borrower]:
    return await borrower_repo.list()


async def create_investor(
    investor: InvestorCreateDTO,
    investor_repo: SqlAlchemyInvestorRepository,
    session: AsyncSession,
) -> None:
    await investor_repo.add(investor)
    await session.commit()
