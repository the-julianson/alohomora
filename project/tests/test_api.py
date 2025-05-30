import logging
import uuid

import pytest


def random_email():
    return f"user-{uuid.uuid4()}@example.com"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_apply_for_loan_end_to_end(client):
    borrower_payload = {
        "name": "John Doe",
        "email": f"user-{uuid.uuid4()}@example.com",
        "income": 150000,
        "employment_years": 5,
        "has_previous_loans": False,
    }

    borrow_resp = client.post("/v1/borrowers", json=borrower_payload)
    assert borrow_resp.status_code == 201
    borrower = borrow_resp.json()

    logger.info(f"Borrower: {borrower}")

    data = {
        "borrower_id": borrower.get("borrower_id", ""),
        "amount": 100000,
        "term_months": 12,
        "purpose": "Home renovation",
    }

    try:
        response = client.post("/v1/loans/apply", json=data)
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response.text}")
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise

    assert response.status_code == 201
    r = response.json()
    assert r["loan_id"] is not None
    assert r["message"] == "Loan applied successfully"


def test_create_borrower_end_to_end(client):
    data = {
        "name": "John Doe",
        "email": random_email(),
        "income": 150000,
        "employment_years": 6,
        "has_previous_loans": False,
    }

    logger.info(f"Request data: {data}")

    response = client.post("/v1/borrowers", json=data)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

    assert response.status_code == 201
    result = response.json()
    logger.info(f"Result: {result}")
    assert "borrower_id" in result
    assert "credit_score" in result
    assert result["credit_score"] == 700
    assert result["message"] == "Borrower created successfully"


def test_create_borrower_with_high_risk_profile(client):
    data = {
        "name": "John Doe",
        "email": random_email(),
        "income": 15000,
        "employment_years": 1,
        "has_previous_loans": True,
    }

    logger.info(f"Request data: {data}")

    response = client.post("/v1/borrowers", json=data)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

    assert response.status_code == 201
    result = response.json()
    assert "borrower_id" in result
    assert "credit_score" in result
    assert result["credit_score"] == 475
    assert result["message"] == "Borrower created successfully"


def test_apply_for_loan_end_to_end_with_bad_credit(client):
    borrower_payload = {
        "name": "John Doe",
        "email": f"user-{uuid.uuid4()}@example.com",
        "income": 500,
        "employment_years": 1,
        "has_previous_loans": True,
    }

    borrow_resp = client.post("/v1/borrowers", json=borrower_payload)
    assert borrow_resp.status_code == 201
    borrower = borrow_resp.json()

    data = {
        "borrower_id": borrower.get("borrower_id", ""),
        "amount": 100000,
        "term_months": 12,
        "purpose": "Home renovation",
    }

    response = client.post("/v1/loans/apply", json=data)
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert "insufficient credit score" in error_detail.lower()
    assert "minimum 600 required" in error_detail.lower()


@pytest.mark.asyncio
async def test_create_investor_async(client):
    response = client.post(
        "/v1/investors",
        json={
            "name": "John Investor",
            "email": "test@example.com",
            "available_funds": 20000,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Investor created successfully"
