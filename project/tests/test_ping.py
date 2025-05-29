# project/tests/test_ping.py


def test_ping(test_app):
    response = test_app.get("/v1/ping")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["environment"] == "dev"
    assert response_json["status"] == "healthy"
    assert response_json["testing"] is True
    assert "web_test" in response_json["database_url"]


def test_version(test_app):
    response = test_app.get("/v1/version")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["version"] == "1.0.0"
    assert response_json["api_version"] == "v1"
    assert response_json["name"] == "Alohomora Loan Management System"
    assert response_json["semantic_version"]["major"] == 1
    assert response_json["semantic_version"]["minor"] == 0
    assert response_json["semantic_version"]["patch"] == 0
