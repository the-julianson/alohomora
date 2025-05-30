import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, repository, services
from app.db import get_async_db_session
from app.models import InsufficientCreditScoreError
from app.services import InvestorCreateDTO


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/v1")


@router.post("/borrowers", status_code=201)
async def create_borrower(
    payload: services.CreateBorrowerDTO,
    session: AsyncSession = Depends(get_async_db_session),
) -> dict:
    logger.info(f"Received borrower creation request: {payload}")
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    try:
        logger.info("About to call create_borrower service")
        borrower_id, credit_score = await services.create_borrower(
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
async def apply(
    payload: services.LoanApplicationDTO,
    session: AsyncSession = Depends(get_async_db_session),
) -> dict:
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)
    borrower = await borrower_repo.get(payload.borrower_id)

    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")

    loan_repo = repository.SqlAlchemyLoanRepository(session)
    loan_object = models.Loan(
        borrower=borrower,
        amount=payload.amount,
        term_months=payload.term_months,
        purpose=payload.purpose,
    )

    try:
        loan_id = await services.apply_for_loan(loan_object, loan_repo, session)
    except InsufficientCreditScoreError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {"loan_id": loan_id, "message": "Loan applied successfully"}


@router.get("/borrowers", status_code=200)
async def get_borrowers(
    session: AsyncSession = Depends(get_async_db_session),
) -> list[dict]:
    borrower_repo = repository.SqlAlchemyBorrowerRepository(session)

    try:
        borrowers = await services.get_borrowers(borrower_repo, session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return [borrower.to_dict() for borrower in borrowers]


@router.post("/investors")
async def create_investor_async(
    payload: InvestorCreateDTO, session: AsyncSession = Depends(get_async_db_session)
):
    investor_repo = repository.SqlAlchemyInvestorRepository(session)

    investor = models.Investor(
        name=payload.name,
        email=payload.email,
        available_funds=payload.available_funds,
    )

    try:
        await services.create_investor(investor, investor_repo, session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {"message": "Investor created successfully"}
