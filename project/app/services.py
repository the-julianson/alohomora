from sqlalchemy.orm import Session

from app.models import Loan, LoanStatus
from app.repository import SqlAlchemyLoanRepository


class LoanApplicationError(Exception):
    pass


def apply_for_loan(
    loan_object: Loan, loan_repo: SqlAlchemyLoanRepository, session: Session
    ) -> str:
    """
    Apply for a new loan with the following rules:
    - If borrower has 2 or more FUNDED or REPAYING loans, reject
    - If borrower has any DEFAULTED loans, reject
    - If borrower has 2 ACTIVE loans, allow up to 4 ACTIVE loans
    - Otherwise, allow the loan
    """
    # Get all loan counts in a single query
    loan_counts = loan_repo.get_loan_counts_by_status(loan_object.borrower.id)

    # Check for defaulted loans
    if loan_counts.get(LoanStatus.DEFAULTED, 0) > 0:
        raise LoanApplicationError("""Cannot apply for loan:
        Borrower has defaulted loans""")

    # Check for funded/repaying loans
    active_loans = (
        loan_counts.get(LoanStatus.FUNDED, 0) +
        loan_counts.get(LoanStatus.REPAYING, 0)
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
    loan_repo.add(loan_object)
    session.commit()
    return loan_object.id
