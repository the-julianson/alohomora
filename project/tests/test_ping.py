# project/tests/test_ping.py


async def test_ping(async_client):
    response = await async_client.get("/v1/ping")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["environment"] == "dev"
    assert response_json["status"] == "healthy"
    assert response_json["testing"] is True
    assert "web_test" in response_json["database_url"]


async def test_version(async_client):
    response = await async_client.get("/v1/version")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["version"] == "1.0.0"
    assert response_json["api_version"] == "v1"
    assert response_json["name"] == "Alohomora Loan Management System"
    assert response_json["semantic_version"]["major"] == 1
    assert response_json["semantic_version"]["minor"] == 0
    assert response_json["semantic_version"]["patch"] == 0
