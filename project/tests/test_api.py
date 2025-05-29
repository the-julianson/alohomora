import logging
import uuid

import requests

from app import config


def random_email():
    return f"user-{uuid.uuid4()}@example.com"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @pytest.mark.usefixtures("restart_api")
def test_apply_for_loan_end_to_end(add_borrower):
    borrower = add_borrower(
        name="John Doe",
        email=random_email(),
        credit_score=700,
    )

    data = {
        "borrower": borrower.to_dict(),
        "amount": 100000,
        "term_months": 12,
        "purpose": "Home renovation",
    }

    url = config.get_api_url()
    logger.info(f"Testing API at {url}")
    try:
        response = requests.post(f"{url}/loans/apply", json=data)
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise

    assert response.status_code == 201
    r = response.json()
    assert r["loan_id"] is not None
    assert r["message"] == "Loan applied successfully"


def test_create_borrower_end_to_end():
    data = {
        "name": "John Doe",
        "email": random_email(),
        "income": 150000,
        "employment_years": 6,
        "has_previous_loans": False,
    }

    url = config.get_api_url()
    logger.info(f"Testing API at {url}")
    logger.info(f"Request data: {data}")

    response = requests.post(f"{url}/borrowers", json=data)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

    assert response.status_code == 201
    result = response.json()
    logger.info(f"Result: {result}")
    assert "borrower_id" in result
    assert "credit_score" in result
    assert result["credit_score"] == 700
    assert result["message"] == "Borrower created successfully"


def test_create_borrower_with_high_risk_profile():
    data = {
        "name": "John Doe",
        "email": random_email(),
        "income": 15000,
        "employment_years": 1,
        "has_previous_loans": True,
    }

    url = config.get_api_url()
    logger.info(f"Testing API at {url}")
    logger.info(f"Request data: {data}")

    response = requests.post(f"{url}/borrowers", json=data)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

    assert response.status_code == 201
    result = response.json()
    assert "borrower_id" in result
    assert "credit_score" in result
    assert result["credit_score"] == 475
    assert result["message"] == "Borrower created successfully"


def test_apply_for_loan_end_to_end_with_bad_credit(add_borrower):
    borrower = add_borrower(
        name="John Doe",
        email=random_email(),
        credit_score=500,
    )

    data = {
        "borrower": borrower.to_dict(),
        "amount": 100000,
        "term_months": 12,
        "purpose": "Home renovation",
    }

    url = config.get_api_url()
    logger.info(f"Testing API at {url}")
    response = requests.post(f"{url}/loans/apply", json=data)
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert "insufficient credit score" in error_detail.lower()
    assert "minimum 600 required" in error_detail.lower()


def test_retrieve_borrowers(add_borrower):
    add_borrower(
        name="John Doe",
        email=random_email(),
        credit_score=700,
    )

    add_borrower(
        name="Jane Doe",
        email=random_email(),
        credit_score=800,
    )

    url = config.get_api_url()
    response = requests.get(f"{url}/borrowers")
    assert response.status_code == 200
    result = response.json()
    assert len(result) > 0
    assert result[0]["name"] == "John Doe"
    assert result[0]["credit_score"] == 700
    assert result[1]["name"] == "Jane Doe"
    assert result[1]["credit_score"] == 800
