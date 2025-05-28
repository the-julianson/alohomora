from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, repository, services
from app.db import get_db_session
from app.models import InsufficientCreditScoreError


router = APIRouter()


class BorrowerDTO(BaseModel):
    id: str
    name: str
    email: str
    credit_score: int


class LoanApplicationDTO(BaseModel):
    borrower: BorrowerDTO
    amount: int
    term_months: int
    purpose: str


@router.post("/loans/apply", status_code=201)
def apply(
    payload: LoanApplicationDTO,
    session: Session = Depends(get_db_session)
    ):
    borrower = models.Borrower(
        id=payload.borrower.id,
        name=payload.borrower.name,
        email=payload.borrower.email,
        credit_score=payload.borrower.credit_score
    )

    loan_repo = repository.SqlAlchemyLoanRepository(session)
    loan_object = models.Loan(
        borrower=borrower,
        amount=payload.amount,
        term_months=payload.term_months,
        purpose=payload.purpose,
    )

    try:
        loan_id = services.apply_for_loan(loan_object, loan_repo, session)
    except InsufficientCreditScoreError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {"loan_id": loan_id, "message": "Loan applied successfully"}
