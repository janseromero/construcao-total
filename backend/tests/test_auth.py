"""Auth: signup, login, me."""

from tests.conftest import auth_headers, signup


def test_signup_login_me(client):
    token = signup(client, cnpj="11222333000144", email="a@a.com")

    r = client.post("/auth/login", json={"email": "a@a.com", "password": "supersecret"})
    assert r.status_code == 200

    r = client.get("/auth/me", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["user"]["email"] == "a@a.com"
    assert r.json()["user"]["role"] == "proprietario"


def test_signup_duplicate_cnpj(client):
    signup(client, cnpj="11222333000155", email="b@b.com")
    r = client.post(
        "/auth/signup",
        json={
            "construtora_nome": "Outra Construtora",
            "cnpj": "11222333000155",
            "user_nome": "Outro Owner",
            "email": "c@c.com",
            "password": "supersecret",
        },
    )
    assert r.status_code == 409


def test_login_wrong_password(client):
    signup(client, cnpj="11222333000166", email="d@d.com")
    r = client.post("/auth/login", json={"email": "d@d.com", "password": "wrong"})
    assert r.status_code == 401
