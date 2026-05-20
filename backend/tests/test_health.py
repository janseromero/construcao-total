"""Health smoke."""


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "Construtor Total"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
