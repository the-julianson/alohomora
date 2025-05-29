# project/tests/test_ping.py


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["environment"] == "dev"
    assert response_json["ping"] == "pong"
    assert response_json["testing"] is True
    assert "web_test" in response_json["database_url"]
