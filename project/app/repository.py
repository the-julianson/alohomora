from typing import List, Optional, Protocol
from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models import Borrower, Investment, Investor, Loan
from app.orm import investments, loans


class LoanRepository(Protocol):
    def add(self, loan: Loan) -> None:
        ...

    def get(self, loan_id: UUID) -> Optional[Loan]:
        ...

    def list(self) -> List[Loan]:
        ...


class BorrowerRepository(Protocol):
    def add(self, borrower: Borrower) -> None:
        ...

    def get(self, borrower_id: UUID) -> Optional[Borrower]:
        ...


class InvestorRepository(Protocol):
    def add(self, investor: Investor) -> None:
        ...

    def get(self, investor_id: UUID) -> Optional[Investor]:
        ...


class InvestmentRepository(Protocol):
    def add(self, investment: Investment) -> None:
        ...

    def get(self, investment_id: UUID) -> Optional[Investment]:
        ...


class SqlAlchemyLoanRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, loan: Loan) -> None:
        stmt = insert(loans).values(
            id = loan.id,
            borrower_id = loan.borrower.id,
            amount = loan.amount,
            purpose = loan.purpose,
            term_months = loan.term_months,
            status = loan.status.value,
        )
        self.session.execute(stmt)

    def get(self, loan_id: UUID) -> Optional[Loan]:
        return self.session.query(Loan).filter_by(id=loan_id).one_or_none()


class SqlAlchemyBorrowerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, borrower: Borrower) -> None:
        self.session.add(borrower)

    def get(self, borrower_id: UUID) -> Optional[Borrower]:
        return self.session.query(Borrower).filter_by(id=borrower_id).one_or_none()


class SqlAlchemyInvestorRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, investor: Investor) -> None:
        self.session.add(investor)

    def get(self, investor_id: UUID) -> Optional[Investor]:
        return self.session.query(Investor).filter_by(id=investor_id).one_or_none()


class SqlAlchemyInvestmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, investment: Investment) -> None:
        stmt = insert(investments).values(
            id = investment.id,
            investor_id = investment.investor.id,
            loan_id = investment.loan.id,
            amount = investment.amount,
            status = investment.status.value,
        )
        self.session.execute(stmt)

    def get(self, investment_id: UUID) -> Optional[Investment]:
        return self.session.query(Investment).filter_by(id=investment_id).one_or_none()
