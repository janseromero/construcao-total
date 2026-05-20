"""Rateio: fração ideal distribui custo corretamente entre unidades."""

from decimal import Decimal

from tests.conftest import auth_headers, signup


def test_rateio_fracao_ideal(client):
    token = signup(client, cnpj="44000000000001", email="rateio@x.com")
    h = auth_headers(token)

    r = client.post("/obras", json={"nome": "Edifício Teste", "uf": "SP"}, headers=h)
    obra_id = r.json()["id"]

    # 2 unidades, frações 0.6 e 0.4
    u1 = client.post(
        f"/obras/{obra_id}/unidades",
        json={"identificador": "101", "fracao_ideal": "0.6", "area_privativa_m2": "60"},
        headers=h,
    ).json()
    u2 = client.post(
        f"/obras/{obra_id}/unidades",
        json={"identificador": "102", "fracao_ideal": "0.4", "area_privativa_m2": "40"},
        headers=h,
    ).json()

    # EAP raiz
    eap = client.post(
        f"/obras/{obra_id}/eap",
        json={"codigo": "1", "nome": "Estrutura", "ordem": 0},
        headers=h,
    ).json()

    # Fornecedor + NF + apropriação de R$ 10.000
    forn = client.post(
        "/fornecedores", json={"nome": "Forn A", "tipo": "material"}, headers=h
    ).json()
    nf = client.post(
        "/notas-fiscais",
        json={
            "obra_id": obra_id,
            "fornecedor_id": forn["id"],
            "numero": "1",
            "data_emissao": "2026-01-15",
            "valor_total": "10000.00",
            "itens": [
                {
                    "descricao": "Cimento",
                    "unidade": "kg",
                    "quantidade": "100",
                    "valor_unitario": "100",
                    "valor_total": "10000.00",
                }
            ],
        },
        headers=h,
    ).json()

    nf_item_id = nf["itens"][0]["id"]
    r = client.post(
        "/apropriacoes",
        json={
            "obra_id": obra_id,
            "eap_id": eap["id"],
            "origem_tipo": "nota_fiscal_item",
            "origem_id": nf_item_id,
            "valor": "10000.00",
            "data_competencia": "2026-01-15",
        },
        headers=h,
    )
    assert r.status_code == 201

    # Recalcular
    r = client.post(f"/obras/{obra_id}/rateio/recalcular", headers=h)
    assert r.status_code == 200

    # Verifica distribuição
    r = client.get(f"/obras/{obra_id}/analise/custo-por-unidade", headers=h)
    assert r.status_code == 200
    rows = {row["unidade_id"]: Decimal(row["custo_acumulado"]) for row in r.json()}
    assert rows[u1["id"]] == Decimal("6000.00")
    assert rows[u2["id"]] == Decimal("4000.00")


def test_apropriacao_excedente_e_bloqueada(client):
    token = signup(client, cnpj="55000000000001", email="ap@x.com")
    h = auth_headers(token)
    obra_id = client.post("/obras", json={"nome": "X", "uf": "SP"}, headers=h).json()["id"]
    eap = client.post(
        f"/obras/{obra_id}/eap", json={"codigo": "1", "nome": "E"}, headers=h
    ).json()
    forn = client.post("/fornecedores", json={"nome": "F", "tipo": "material"}, headers=h).json()
    nf = client.post(
        "/notas-fiscais",
        json={
            "obra_id": obra_id,
            "fornecedor_id": forn["id"],
            "numero": "1",
            "data_emissao": "2026-01-01",
            "valor_total": "100.00",
            "itens": [
                {
                    "descricao": "X",
                    "unidade": "un",
                    "quantidade": "1",
                    "valor_unitario": "100",
                    "valor_total": "100.00",
                }
            ],
        },
        headers=h,
    ).json()
    item_id = nf["itens"][0]["id"]

    r = client.post(
        "/apropriacoes",
        json={
            "obra_id": obra_id,
            "eap_id": eap["id"],
            "origem_tipo": "nota_fiscal_item",
            "origem_id": item_id,
            "valor": "150.00",
            "data_competencia": "2026-01-01",
        },
        headers=h,
    )
    assert r.status_code == 400
