"""Operacional não pode ver margem nem vendas."""

from uuid import UUID

from app.core.security import hash_password
from app.models.user import User, UserRole
from tests.conftest import auth_headers, signup


def _make_operacional(db, tenant_id, *, email="op@x.com"):
    if isinstance(tenant_id, str):
        tenant_id = UUID(tenant_id)
    u = User(
        tenant_id=tenant_id,
        email=email,
        nome="Op",
        senha_hash=hash_password("supersecret"),
        role=UserRole.operacional,
        ativo=True,
    )
    db.add(u)
    db.commit()
    return u


def test_operacional_bloqueado_em_vendas_e_margem(client, db):
    token = signup(client, cnpj="66000000000001", email="prop@x.com")
    h_prop = auth_headers(token)

    me = client.get("/auth/me", headers=h_prop).json()
    tenant_id = me["user"]["tenant_id"]
    _make_operacional(db, tenant_id)

    r = client.post("/auth/login", json={"email": "op@x.com", "password": "supersecret"})
    op_token = r.json()["access_token"]
    h_op = auth_headers(op_token)

    obra_id = client.post("/obras", json={"nome": "O", "uf": "SP"}, headers=h_prop).json()["id"]

    # Operacional pode ver custo por unidade (sem margem)
    r = client.get(f"/obras/{obra_id}/analise/custo-por-unidade", headers=h_op)
    assert r.status_code == 200

    # Mas NÃO pode ver margem
    r = client.get(f"/obras/{obra_id}/analise/margem-por-unidade", headers=h_op)
    assert r.status_code == 403

    # Nem listar vendas
    r = client.get("/vendas", headers=h_op)
    assert r.status_code == 403

    # Nem listar compradores
    r = client.get("/compradores", headers=h_op)
    assert r.status_code == 403

    # Resumo executivo: 403
    r = client.get(f"/obras/{obra_id}/analise/resumo", headers=h_op)
    assert r.status_code == 403


def test_apontamento_oculta_valor_para_operacional(client, db):
    token = signup(client, cnpj="77000000000001", email="prop2@x.com")
    h_prop = auth_headers(token)

    me = client.get("/auth/me", headers=h_prop).json()
    tenant_id = me["user"]["tenant_id"]
    _make_operacional(db, tenant_id, email="op2@x.com")
    op_token = client.post(
        "/auth/login", json={"email": "op2@x.com", "password": "supersecret"}
    ).json()["access_token"]
    h_op = auth_headers(op_token)

    obra_id = client.post("/obras", json={"nome": "O2", "uf": "SP"}, headers=h_prop).json()["id"]
    eap = client.post(
        f"/obras/{obra_id}/eap", json={"codigo": "1", "nome": "E"}, headers=h_prop
    ).json()
    insumo = client.post(
        "/insumos",
        json={
            "codigo": "MO-PED",
            "descricao": "Pedreiro",
            "unidade": "h",
            "tipo": "mao_obra",
            "custo_unitario_referencia": "50",
        },
        headers=h_prop,
    ).json()

    r = client.post(
        "/apontamentos",
        json={
            "obra_id": obra_id,
            "eap_id": eap["id"],
            "data": "2026-01-10",
            "insumo_id": insumo["id"],
            "quantidade": "8",
        },
        headers=h_op,
    )
    assert r.status_code == 201
    # Valor NÃO retornado para operacional
    assert r.json()["valor_total"] is None

    # Proprietário VÊ o valor
    r = client.get(f"/apontamentos?obra_id={obra_id}", headers=h_prop)
    assert r.status_code == 200
    assert any(a["valor_total"] is not None for a in r.json())
