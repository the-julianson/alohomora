
from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import mapper, relationship

from .domain.entities import (
    Borrower,
    Investment,
    InvestmentStatus,
    Investor,
    Loan,
    LoanStatus,
)


metadata = MetaData()

borrowers = Table(
    "borrowers",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("credit_score", Integer, nullable=False),
)

investors = Table(
    "investors",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("available_funds", Numeric(10, 2), nullable=False),
)

loans = Table(
    "loans",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("borrower_id", ForeignKey("borrowers.id"), nullable=False),
    Column("amount", Numeric(10, 2), nullable=False),
    Column("purpose", String(255), nullable=False),
    Column("term_months", Integer, nullable=False),
    Column("status", Enum(LoanStatus), nullable=False),
    Column("created_at", Date, nullable=False),
)

investments = Table(
    "investments",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("investor_id", ForeignKey("investors.id"), nullable=False),
    Column("loan_id", ForeignKey("loans.id"), nullable=False),
    Column("amount", Numeric(10, 2), nullable=False),
    Column("status", Enum(InvestmentStatus), nullable=False),
    Column("created_at", Date, nullable=False),
)

repayments = Table(
    "repayments",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("investment_id", ForeignKey("investments.id"), nullable=False),
    Column("amount", Numeric(10, 2), nullable=False),
    Column("created_at", Date, nullable=False),
)


def start_mappers():
    borrower_mapper = mapper(Borrower, borrowers)
    investor_mapper = mapper(Investor, investors)

    loan_mapper = mapper(
        Loan,
        loans,
        properties={
            "borrower": relationship(borrower_mapper),
            "investment": relationship(
                "Investment",
                uselist=False,
                back_populates="loan"
            )
        }
    )

    investment_mapper = mapper(
        Investment,
        investments,
        properties={
            "investor": relationship(investor_mapper),
            "loan": relationship(loan_mapper, back_populates="investment"),
            "repayments": relationship("Repayment", back_populates="investment")
        }
    )

    mapper(
        "Repayment",
        repayments,
        properties={
            "investment": relationship(investment_mapper, back_populates="repayments")
        }
    )
