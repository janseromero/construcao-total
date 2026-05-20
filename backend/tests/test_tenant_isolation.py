"""Garante que tenants não veem recursos uns dos outros."""

from tests.conftest import auth_headers, signup


def test_obras_isolation(client):
    t1 = signup(client, cnpj="22000000000111", email="t1@x.com")
    t2 = signup(client, cnpj="33000000000111", email="t2@x.com")

    r = client.post(
        "/obras",
        json={"nome": "Obra A", "uf": "SP"},
        headers=auth_headers(t1),
    )
    assert r.status_code == 201
    obra_id = r.json()["id"]

    # Tenant 2 não vê a obra do tenant 1
    r = client.get("/obras", headers=auth_headers(t2))
    assert r.status_code == 200
    assert all(o["id"] != obra_id for o in r.json())

    # E não pode acessá-la diretamente
    r = client.get(f"/obras/{obra_id}", headers=auth_headers(t2))
    assert r.status_code == 404


def test_unauthenticated_blocked(client):
    r = client.get("/obras")
    assert r.status_code == 401
