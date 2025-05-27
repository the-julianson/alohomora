from decimal import Decimal

from sqlalchemy import text

from app import models, repository


def test_repository_can_save_a_loan(session):
    borrower = models.Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    borrower_repo.add(borrower)
    session.commit()

    borrower_rows = list(session.execute(
        text(
            """
            SELECT * FROM borrowers
            """
        )
    ))
    assert borrower_rows == [
        (borrower.id, "John Doe", "john@example.com", 700)
    ]

    loan = models.Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
    )
    repo = repository.SqlAlchemyLoanRepository(session)
    repo.add(loan)
    session.commit()

    rows = list(session.execute(
        text("SELECT borrower_id, amount, purpose, term_months FROM loans")
    ))

    borrower_id, amount, purpose, term_months = rows[0]

    assert str(loan.borrower.id) == str(borrower_id)
    assert loan.amount == Decimal(amount)
    assert loan.purpose == purpose
    assert loan.term_months == term_months


def test_repository_can_save_an_investment(session):
    # Create an investor and commit
    investor = models.Investor(
        name="Warren Buffet",
        email="warren@example.com",
        available_funds=Decimal("1500")
    )
    investor_repo = repository.SqlAlchemyInvestorRepository(session)
    investor_repo.add(investor)
    session.commit()

    investor_from_db = investor_repo.get(investor_id=investor.id)
    session.commit()

    assert investor_from_db.id == investor.id

    # Create a Borrower and commit
    borrower = models.Borrower(
        name="John Doe", email="john@example.com", credit_score=700
    )
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    borrower_repo.add(borrower)
    session.commit()
    borrower_from_db = borrower_repo.get(borrower_id=borrower.id)
    session.commit()
    assert borrower_from_db == borrower


    # Create a Loan, assign the borrow to it and commit
    loan = models.Loan(
        borrower=borrower,
        amount=Decimal("1000.00"),
        purpose="Home improvement",
        term_months=12,
    )
    repo_loan = repository.SqlAlchemyLoanRepository(session)
    repo_loan.add(loan)
    session.commit()
    loan_from_db = repo_loan.get(loan_id=loan.id)
    assert loan_from_db.borrower.id == borrower.id
    assert loan_from_db.purpose == loan.purpose
    assert loan_from_db.amount == loan.amount

    # Create an Investment, assign the investor and loan to it and commit
    investment = models.Investment(
        investor=investor,
        loan=loan,
        amount=loan.amount
    )
    investment_repo = repository.SqlAlchemyInvestmentRepository(session)
    investment_repo.add(investment)
    session.commit()
    # Verify the investment is saved correctly

    investment_from_db = investment_repo.get(investment_id=investment.id)
    assert investment_from_db.investor.id == investor.id
    assert investment_from_db.loan.id == loan.id
    assert investment_from_db.amount == investment.amount
    assert investment_from_db.status == investment.status






