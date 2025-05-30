from typing import Protocol
from uuid import UUID

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Borrower, Investment, Investor, Loan, LoanStatus
from app.orm import borrowers, investments, investors, loans


class LoanRepository(Protocol):
    async def add(self, loan: Loan) -> None: ...

    async def get(self, loan_id: UUID) -> Loan | None: ...

    async def list(self) -> list[Loan]: ...

    async def get_loan_counts_by_status(
        self, borrower_id: UUID
    ) -> dict[LoanStatus, int]: ...


class BorrowerRepository(Protocol):
    async def add(self, borrower: Borrower) -> None: ...

    async def get(self, borrower_id: UUID) -> Borrower | None: ...

    async def list(self) -> list[Loan]: ...


class InvestorRepository(Protocol):
    async def add(self, investor: Investor) -> None: ...

    async def get(self, investor_id: UUID) -> Investor | None: ...


class InvestmentRepository(Protocol):
    async def add(self, investment: Investment) -> None: ...

    async def get(self, investment_id: UUID) -> Investment | None: ...


class SqlAlchemyLoanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, loan: Loan) -> None:
        stmt = insert(loans).values(
            id=loan.id,
            borrower_id=loan.borrower.id,
            amount=loan.amount,
            purpose=loan.purpose,
            term_months=loan.term_months,
            status=loan.status.value,
        )
        self.session.execute(stmt)

    async def get(self, loan_id: UUID) -> Loan | None:
        stmt = select(Loan).where(Loan.id == loan_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        borrower_id: UUID | None = None,
        status: LoanStatus | None = None,
    ) -> list[Loan]:
        """
        List loans with optional filters.
        Used to check borrower's loan history and status.
        """
        query = select(Loan)

        if borrower_id is not None:
            query = query.where(Loan.borrower_id == borrower_id)
        if status is not None:
            query = query.where(Loan.status == status)
        return self.session.execute(query).scalars().all()

    async def get_loan_counts_by_status(
        self, borrower_id: UUID
    ) -> dict[LoanStatus, int]:
        """
        Get counts of loans by status for a borrower in a single query.
        Returns a dictionary mapping status to count.
        """
        query = (
            select(Loan.status, func.count(Loan.id).label("count"))
            .where(Loan.borrower_id == borrower_id)
            .group_by(Loan.status)
        )
        result = await self.session.execute(query)
        result = result.all()
        # Convert result to dictionary, defaulting to 0 for missing statuses
        return dict(result)


class SqlAlchemyBorrowerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, borrower: Borrower) -> None:
        stmt = insert(borrowers).values(
            id=borrower.id,
            name=borrower.name,
            email=borrower.email,
            credit_score=borrower.credit_score,
        )
        await self.session.execute(stmt)

    async def get(self, borrower_id: UUID) -> Borrower | None:
        stmt = select(Borrower).where(Borrower.id == borrower_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self) -> list[Borrower]:
        stmt = select(Borrower)
        result = await self.session.execute(stmt)
        existing = result.scalars().all()
        return existing


class SqlAlchemyInvestorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, investor: Investor) -> None:
        stmt = insert(investors).values(
            id=investor.id,
            name=investor.name,
            email=investor.email,
            available_funds=investor.available_funds,
        )
        await self.session.execute(stmt)

    async def get(self, investor_id: UUID) -> Investor | None:
        stmt = select(Investor).where(Investor.id == investor_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SqlAlchemyInvestmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, investment: Investment) -> None:
        stmt = insert(investments).values(
            id=investment.id,
            investor_id=investment.investor.id,
            loan_id=investment.loan.id,
            amount=investment.amount,
            status=investment.status.value,
        )
        await self.session.execute(stmt)

    async def get(self, investment_id: UUID) -> Investment | None:
        stmt = select(Investment).where(Investment.id == investment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
