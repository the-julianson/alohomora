from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry, relationship

from .models import (
    Borrower,
    Investment,
    InvestmentStatus,
    Investor,
    Loan,
    LoanStatus,
    Repayment,
)


metadata = MetaData()
mapper_registry = registry()

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
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)

investments = Table(
    "investments",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("investor_id", ForeignKey("investors.id"), nullable=False),
    Column("loan_id", ForeignKey("loans.id"), nullable=False),
    Column("amount", Numeric(10, 2), nullable=False),
    Column("status", Enum(InvestmentStatus), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)

repayments = Table(
    "repayments",
    metadata,
    Column("id", String(36), primary_key=True),  # UUID as string
    Column("investment_id", ForeignKey("investments.id"), nullable=False),
    Column("amount", Numeric(10, 2), nullable=False),
    Column("created_at", Date, nullable=False, server_default=func.now()),
)


def start_mappers():
    mapper_registry.dispose()

    mapper_registry.map_imperatively(
        Borrower,
        borrowers,
        properties={"loans": relationship(Loan, back_populates="borrower")},
    )

    mapper_registry.map_imperatively(
        Investor,
        investors,
        properties={"investments": relationship(Investment, back_populates="investor")},
    )

    mapper_registry.map_imperatively(
        Loan,
        loans,
        properties={
            "borrower": relationship(Borrower, back_populates="loans"),
            "investment": relationship(
                Investment, uselist=False, back_populates="loan"
            ),
        },
    )

    mapper_registry.map_imperatively(
        Investment,
        investments,
        properties={
            "investor": relationship(Investor, back_populates="investments"),
            "loan": relationship(Loan, back_populates="investment"),
            "repayments": relationship(Repayment, back_populates="investment"),
        },
    )

    # ← use the class Repayment here, not a string
    mapper_registry.map_imperatively(
        Repayment,
        repayments,
        properties={
            "investment": relationship(Investment, back_populates="repayments")
        },
    )
