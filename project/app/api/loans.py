import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, repository, services
from app.db import get_db_session
from app.models import InsufficientCreditScoreError


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/borrowers", status_code=201)
def create_borrower(
    payload: services.CreateBorrowerDTO, session: Session = Depends(get_db_session)
):
    logger.info(f"Received borrower creation request: {payload}")
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    try:
        logger.info("About to call create_borrower service")
        borrower_id, credit_score = services.create_borrower(
            prospect_borrower=payload, borrower_repo=borrower_repo, session=session
        )
        logger.info(f"""Successfully created borrower with ID
        {borrower_id} and credit score {credit_score}""")
        return {
            "borrower_id": borrower_id,
            "credit_score": credit_score,
            "message": "Borrower created successfully",
        }
    except Exception as e:
        logger.error(f"Error creating borrower: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/loans/apply", status_code=201)
def apply(
    payload: services.LoanApplicationDTO, session: Session = Depends(get_db_session)
):
    borrower = models.Borrower(
        id=payload.borrower.id,
        name=payload.borrower.name,
        email=payload.borrower.email,
        credit_score=payload.borrower.credit_score,
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
