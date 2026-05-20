# 2. Obras e unidades

A **obra** é a entidade central do sistema. Toda informação — orçamento, custo, venda — pendura nela. Neste capítulo você cria a obra, define os tipos de apartamento (tipologias) e cadastra cada apartamento (unidade) com sua fração ideal.

---

## 2.1. O que é uma obra no Construtor Total

Uma obra representa um **empreendimento** — um prédio, um conjunto de casas, uma reforma grande. No MVP, recomendamos rodar **uma obra por vez** no sistema; multi-obras com rateio cruzado entram em versões futuras.

Cada obra tem:
- **Identidade:** nome, endereço, UF (estado).
- **Datas:** início e fim previstos e reais.
- **Áreas:** total construída (m²) e do terreno (m²).
- **Status:** planejamento, em obra, concluída, pausada.
- **Em afetação:** flag para Patrimônio de Afetação (fora do MVP, fica de gancho).

---

## 2.2. Criar a obra

1. No menu lateral, clique em **Obras**.
2. Clique em **Nova obra** (botão amarelo, canto superior direito).
3. Preencha:
   - **Nome** — ex.: `Residencial Aurora`.
   - **Endereço** — opcional, mas recomendado.
   - **UF** — obrigatório, define qual tabela SINAPI será usada (a SINAPI varia por estado).
   - **Status** — comece com `planejamento`; mude para `em_obra` quando começar a execução.
   - **Início previsto / Fim previsto** — datas planejadas.
   - **Área construída (m²)** — soma de áreas privativas + áreas comuns.
   - **Área terreno (m²)** — área do lote.
4. Clique em **Criar obra**.

Você é redirecionado para a **Visão geral** da obra recém-criada.

💡 **A regra de rateio padrão é criada automaticamente:** "obra inteira, por fração ideal". Se você não mexer em mais nada, todo custo lançado será distribuído entre as unidades proporcionalmente à fração ideal.

### Exemplo prático — Residencial Aurora

| Campo | Valor |
|-------|-------|
| Nome | Residencial Aurora |
| Endereço | Rua das Acácias, 250 — Vila Olímpia — São Paulo/SP |
| UF | SP |
| Status | em_obra |
| Início previsto | 2026-03-01 |
| Fim previsto | 2027-12-15 |
| Área construída | 1.040,00 m² |
| Área terreno | 480,00 m² |

---

## 2.3. Tipologias — os modelos de apartamento

Uma **tipologia** é um modelo de unidade: "Tipo A — 2 dormitórios, 60 m²". Você cadastra tipologias quando seu prédio tem unidades repetidas (o que é a regra geral).

⚠️ Tipologia é uma conveniência — facilita criar unidades em massa. Cada unidade pode ter sua área editada depois, independente da tipologia.

### Como criar tipologia

A criação de tipologia entra como detalhe da tela de **Unidades** na Onda 2. No MVP atual, tipologias são opcionais — você pode cadastrar unidades diretamente sem tipologia. Quando precisar, use a API:

```bash
POST /obras/{obra_id}/tipologias
{
  "nome": "Tipo A — 2 dorm",
  "area_privativa_m2": 60.00,
  "area_comum_proporcional_m2": 25.00
}
```

### Exemplo Residencial Aurora — 2 tipologias

| Tipologia | Área privativa | Área comum proporcional |
|-----------|----------------|--------------------------|
| Tipo A — 2 dorm | 60,00 m² | 25,00 m² |
| Tipo B — 3 dorm | 85,00 m² | 30,00 m² |

---

## 2.4. Unidades — os apartamentos individuais

A **unidade** é cada apartamento físico. Cada unidade tem:
- **Identificador** — como você chama no dia a dia: `101`, `Apto 502 Bloco B`, etc.
- **Andar** — opcional.
- **Bloco** — opcional, para empreendimentos com mais de um bloco.
- **Tipologia** — opcional, modelo de referência.
- **Fração ideal** — o número mais importante.
- **Área privativa (m²)** — pode herdar da tipologia ou ser editada por unidade.

### O que é fração ideal

A **fração ideal** é o **percentual legal** que cada unidade tem do terreno e das áreas comuns. É definida na convenção de condomínio e no projeto aprovado. Ela serve para:
- Rateio das despesas comuns do prédio (legal).
- **Rateio do custo da obra entre as unidades**, no Construtor Total (default).

⚠️ A **soma das frações ideais de todas as unidades de uma obra deve ser igual a 1,0** (ou 100%, dependendo da unidade). O sistema mostra um alerta amarelo se a soma não bater.

💡 A fração ideal **não é** necessariamente igual à área privativa dividida pela área total — ela é definida pelo memorial descritivo e pode considerar áreas comuns de uso exclusivo, posição no prédio, etc.

### Como cadastrar unidades

1. Entre na obra → aba **Unidades**.
2. Clique em **Nova unidade**.
3. Preencha:
   - **Identificador** — obrigatório, ex.: `101`.
   - **Andar** — opcional, ex.: `1`.
   - **Bloco** — opcional.
   - **Fração ideal** — número entre 0 e 1, com até 8 casas decimais. Ex.: `0.12500000`.
   - **Área privativa (m²)** — ex.: `60.00`.
4. Clique em **Salvar**.

Repita para cada apartamento.

💡 No rodapé da tabela, o sistema mostra a **soma das frações ideais**. Use isso pra conferir que está fechando em 1,0.

### Exemplo Residencial Aurora — 8 unidades

| Identificador | Andar | Tipologia | Fração ideal | Área (m²) |
|---------------|-------|-----------|--------------|-----------|
| 101 | 1 | Tipo A | 0,11000000 | 60,00 |
| 102 | 1 | Tipo A | 0,11000000 | 60,00 |
| 201 | 2 | Tipo A | 0,11500000 | 60,00 |
| 202 | 2 | Tipo A | 0,11500000 | 60,00 |
| 301 | 3 | Tipo B | 0,14000000 | 85,00 |
| 302 | 3 | Tipo B | 0,14000000 | 85,00 |
| 401 | 4 | Tipo B (cobertura) | 0,13500000 | 85,00 |
| 402 | 4 | Tipo B (cobertura) | 0,13500000 | 85,00 |
| **Total** | | | **1,00000000** | **580,00** |

Note que andares mais altos têm fração ideal maior — é uma convenção comum (vista, conforto). E os 580 m² privativos não batem com os 1.040 m² da obra: a diferença são as áreas comuns (escada, hall, garagem, área de lazer).

---

## 2.5. Editar e remover

- **Editar** — não há tela dedicada no MVP. Para mudar uma unidade, remova e crie de novo, ou edite via API: `PUT /obras/{obra_id}/unidades/{unidade_id}`.
- **Remover** — botão **Remover** na linha da unidade. Confirma antes.

⚠️ Não remova unidades depois que já houver vendas registradas — o sistema vai bloquear. Marque como `distratada` no módulo de Vendas.

---

## 2.6. Mudar status da obra

Conforme a obra avança, mude o status:
- `planejamento` → enquanto está montando orçamento, EAP, definindo unidades.
- `em_obra` → quando a execução começou de fato.
- `concluida` → quando entregou.
- `pausada` → em caso de paralisação.

Para editar o status no MVP, use a API `PUT /obras/{id}` ou aguarde a tela de edição da Onda 2.

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Soma de frações ideais com ⚠ ≠ 1,0000 | Esqueceu alguma unidade ou erro de digitação | Conferir cada unidade; total deve fechar em 1,0 |
| Não consigo remover unidade | Há venda ou apropriação ligada | Remova venda primeiro, ou marque como distratada |
| Fração ideal aceitando até 8 casas | Sim, é proposital | Use pelo menos 6 casas para evitar arredondamento que deixa total ≠ 1 |
| Área da obra ≠ soma de áreas das unidades | Normal — diferença são áreas comuns | Não é erro |

---

**Próximo passo:** [Capítulo 3 — EAP](03-eap.md), onde você monta a árvore de etapas da obra que vai ancorar todo o orçamento e todos os custos.
