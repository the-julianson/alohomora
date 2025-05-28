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
        response = requests.post(
            f"{url}/loans/apply", json=data
        )
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise

    assert response.status_code == 201
    r = response.json()
    assert r["loan_id"] is not None
    assert r["message"] == "Loan applied successfully"


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
    response = requests.post(
        f"{url}/loans/apply", json=data
    )
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert "insufficient credit score" in error_detail.lower()
    assert "minimum 600 required" in error_detail.lower()
