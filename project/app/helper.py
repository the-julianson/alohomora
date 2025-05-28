# app/helper.py

import logging


logger = logging.getLogger(__name__)


def calculate_credit_score(
    income: int, employment_years: int, has_previous_loans: bool
) -> int:
    """
    Calculate credit score based on borrower's profile.
    This is a simplified version that could be replaced with a more sophisticated
    scoring system or external service in the future.
    """
    logger.info(f"""Calculating credit score for income={income},
    employment_years={employment_years},
    has_previous_loans={has_previous_loans}""")
    base_score = 500
    # Income factor (0-100 points)
    income_score = min(income // 1000, 200)
    # Employment stability factor (0-50 points)
    employment_score = min(employment_years * 10, 50)
    # Previous loans factor (-50 to 0 points)
    previous_loans_score = -50 if has_previous_loans else 0
    final_score = base_score + income_score + employment_score + previous_loans_score
    logger.info(f"Calculated credit score: {final_score}")
    return final_score
