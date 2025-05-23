from typing import List, Optional, Protocol
from uuid import UUID

from app.models import Borrower, Investment, Investor, Loan


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
