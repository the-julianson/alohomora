from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class LoanStatus(str, Enum):
    ACTIVE = "active"
    FUNDED = "funded"
    REPAYING = "repaying"
    PAID = "paid"
    DEFAULTED = "defaulted"


class InvestmentStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    REJECTED = "rejected"
    COMPLETED = "completed"


class InsufficientFundsError(Exception):
    pass


class InvalidInvestmentAmountError(Exception):
    pass


class LoanAlreadyFundedError(Exception):
    pass


@dataclass
class Borrower:
    name: str
    email: str
    credit_score: int
    id: UUID = uuid4()

    def can_create_loan(self) -> bool:
        return self.credit_score >= 600


@dataclass
class Loan:
    borrower: Borrower
    amount: Decimal
    purpose: str
    term_months: int
    id: UUID = uuid4()
    status: LoanStatus = LoanStatus.ACTIVE
    created_at: datetime = datetime.now()
    investment: Optional["Investment"] = None

    def can_accept_investment(self, amount: Decimal) -> bool:
        return (
            self.status == LoanStatus.ACTIVE
            and self.investment is None
            and amount == self.amount
        )

    def accept_investment(self, investment: "Investment") -> None:
        if not self.can_accept_investment(investment.amount):
            raise LoanAlreadyFundedError(f"Loan {self.id} cannot accept investment")
        self.investment = investment
        self.status = LoanStatus.FUNDED

    def reject_investment(self) -> None:
        if (
            self.investment
            and self.investment.status == InvestmentStatus.PENDING_APPROVAL
        ):
            self.investment = None
            self.status = LoanStatus.ACTIVE


@dataclass
class Investor:
    name: str
    email: str
    available_funds: Decimal
    id: UUID = uuid4()

    def can_invest(self, amount: Decimal) -> bool:
        return self.available_funds >= amount

    def invest(self, amount: Decimal) -> None:
        if not self.can_invest(amount):
            raise InsufficientFundsError(
                f"Insufficient funds for investment of {amount}"
            )
        self.available_funds -= amount

    def refund(self, amount: Decimal) -> None:
        self.available_funds += amount


@dataclass
class Investment:
    investor: Investor
    loan: Loan
    amount: Decimal
    status: InvestmentStatus = InvestmentStatus.PENDING_APPROVAL
    created_at: datetime = datetime.now()
    repayments: list["Repayment"] = None
    id: UUID = uuid4()

    def __post_init__(self):
        if self.repayments is None:
            self.repayments = []

    def validate_amount(self) -> None:
        if self.amount != self.loan.amount:
            raise InvalidInvestmentAmountError(
                f"Investment amount {self.amount} must match "
                f"loan amount {self.loan.amount}"
            )

    def approve(self) -> None:
        if self.status != InvestmentStatus.PENDING_APPROVAL:
            raise ValueError("Can only approve pending investments")
        self.status = InvestmentStatus.ACTIVE
        self.loan.accept_investment(self)

    def reject(self) -> None:
        if self.status != InvestmentStatus.PENDING_APPROVAL:
            raise ValueError("Can only reject pending investments")
        self.status = InvestmentStatus.REJECTED
        self.investor.refund(self.amount)
        self.loan.reject_investment()

    @property
    def remaining_amount(self) -> Decimal:
        return self.amount - sum(rep.amount for rep in self.repayments)


@dataclass
class Repayment:
    investment: Investment
    amount: Decimal
    paid_at: datetime = datetime.now()
    id: UUID = uuid4()

    def validate_amount(self) -> None:
        if self.amount > self.investment.remaining_amount:
            raise ValueError(
                "Repayment amount exceeds remaining investment amount"
            )
