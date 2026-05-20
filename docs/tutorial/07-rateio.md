# 7. Rateio

O rateio é como o sistema **distribui o custo da obra entre os apartamentos**. É a mágica que transforma "gastei R$ 1.500.000 na obra" em "o apto 101 me custou R$ 165.000".

Sem rateio, você sabe o custo da obra; com rateio, você sabe o custo de **cada unidade**.

---

## 7.1. Conceito

Toda **apropriação** (capítulo 6) lança um valor em uma folha da EAP. O rateio responde: "este valor da apropriação pertence a quais unidades, e em que proporção?"

Exemplo: uma NF de R$ 10.000 em `3.3 Lajes` precisa ser dividida entre as 8 unidades. Como?

A resposta depende do **critério de rateio**:

| Critério | Como divide |
|----------|-------------|
| **Fração ideal** | Proporcional à fração ideal de cada unidade (default) |
| **Área privativa** | Proporcional à área privativa (m²) |
| **Igualitário** | Divide em partes iguais entre as unidades |
| **Customizado** | Pesos definidos por você, unidade a unidade |

---

## 7.2. Regra geral vs. regra por EAP

Quando você cria uma obra, o sistema cria automaticamente uma **regra geral**:

> **Escopo:** obra inteira. **Critério:** fração ideal.

Isso significa: **todo** custo apropriado em qualquer etapa será rateado entre **todas** as unidades, na proporção da fração ideal de cada uma.

Mas você pode criar **regras específicas** para sub-árvores da EAP. Exemplos:

- **Cobertura** (`5. Cobertura`) — só os apartamentos do último andar deveriam pagar.
- **Garagem** (`10.3 Garagem`) — só os apartamentos que têm vaga.
- **Lazer / piscina** — todos os apartamentos pagam igual (não proporcional ao tamanho).

### Como o sistema resolve qual regra aplicar

Para cada apropriação:

1. Procura uma regra com `escopo = EAP` para a folha da apropriação. Se achar, usa.
2. Se não achar, sobe na árvore EAP e procura no pai. E no avô. Etc.
3. Se nenhum ancestral tem regra específica, usa a **regra geral da obra**.

💡 É como CSS: a regra mais específica vence.

---

## 7.3. Definir uma regra específica por EAP (via API no MVP)

A tela completa de regras de rateio entra na Onda 2. No MVP:

```bash
# Regra específica para áreas comuns/lazer — igualitário
POST /obras/{obra_id}/rateio/regras
{
  "escopo_tipo": "eap",
  "escopo_eap_id": "<id de 10.4 Paisagismo>",
  "criterio": "igualitario"
}

# Regra para coberturas — customizada com pesos só nos aptos do último andar
POST /obras/{obra_id}/rateio/regras
{
  "escopo_tipo": "eap",
  "escopo_eap_id": "<id de 5. Cobertura>",
  "criterio": "customizado",
  "pesos": [
    {"unidade_id": "<id apto 401>", "peso": 1.0},
    {"unidade_id": "<id apto 402>", "peso": 1.0}
  ]
}
```

Quando outros apartamentos têm `peso = 0` (ou não aparecem na lista), eles **não são rateados** para essa etapa.

---

## 7.4. Cálculo passo a passo

Exemplo: 8 unidades, R$ 10.000 apropriados em `3.3 Lajes`, regra geral = fração ideal.

### Pesos (frações ideais)

| Unidade | Fração ideal |
|---------|--------------|
| 101 | 0,110 |
| 102 | 0,110 |
| 201 | 0,115 |
| 202 | 0,115 |
| 301 | 0,140 |
| 302 | 0,140 |
| 401 | 0,135 |
| 402 | 0,135 |
| **Soma** | **1,000** |

### Distribuição

| Unidade | Cálculo | Quota (R$) |
|---------|---------|------------|
| 101 | 10.000 × (0,110 / 1,000) | 1.100,00 |
| 102 | 10.000 × (0,110 / 1,000) | 1.100,00 |
| 201 | 10.000 × (0,115 / 1,000) | 1.150,00 |
| 202 | 10.000 × (0,115 / 1,000) | 1.150,00 |
| 301 | 10.000 × (0,140 / 1,000) | 1.400,00 |
| 302 | 10.000 × (0,140 / 1,000) | 1.400,00 |
| 401 | 10.000 × (0,135 / 1,000) | 1.350,00 |
| 402 | 10.000 × (0,135 / 1,000) | 1.350,00 |
| **Total** | | **10.000,00** |

Os pesos são **normalizados** (divididos pela soma), então mesmo que a soma das frações não dê exatamente 1,0, o rateio funciona — só a proporção importa.

### O que acontece quando se acumulam várias apropriações

Cada apropriação é rateada individualmente, e o sistema **soma** as quotas por unidade. No final, você tem:

```
Custo acumulado do apto 101 = soma de todas as quotas que caíram nele
```

Isso é o que aparece em **Análise → Custo por unidade**.

---

## 7.5. Quando recalcular

O cache de rateio (`rateio_calculado`) é atualizado em três situações:

1. **Automático ao abrir a tela de Análise → Custo por unidade** — o sistema recalcula antes de mostrar.
2. **Manual** — botão **Recalcular rateio** na aba Análise da obra.
3. **Quando você muda regras de rateio** — recalcule depois.

💡 Para uma obra com 100 unidades e milhares de apropriações, o recálculo deve rodar em menos de 5 segundos. Se demora mais, abra ticket técnico.

---

## 7.6. Critério: qual escolher

### Fração ideal (default)

**Use quando:** rateio normal entre apartamentos de tamanhos diferentes. É a forma mais justa quando os apartamentos refletem na fração ideal o seu valor relativo no empreendimento (o que é o caso na maioria das incorporações).

### Área privativa

**Use quando:** quer um critério puramente proporcional ao tamanho. Diferença sutil em relação à fração ideal — a fração ideal pode considerar fatores além do tamanho (vista, andar, posição).

### Igualitário

**Use quando:** o custo não tem relação com o tamanho. Exemplos:
- Lazer (piscina, churrasqueira) — todo apartamento usa igual.
- Portaria, salão de festas — uso comum sem proporção.
- Documentação e taxas iniciais — alvará, ART.

### Customizado

**Use quando:** só um subconjunto de unidades é beneficiado:
- **Cobertura** — só os apartamentos do último andar.
- **Garagem extra** — só apartamentos que compraram vaga adicional.
- **Sacada gourmet** — só os apartamentos que têm.

---

## 7.7. Estratégia de regras para uma obra residencial

Recomendação padrão:

1. **Regra geral** — `obra_inteira` + `fracao_ideal` (já é o default).
2. **Áreas comuns de lazer** — `igualitario` para `10.4 Paisagismo`, `10.5 Lazer` (se houver).
3. **Cobertura** — `customizado` com pesos só nos aptos do último andar.
4. **Custos indiretos** (`12.*`) — geralmente `fracao_ideal` mesmo, ou `igualitario` se preferir.

Não invente regras demais. Cada regra extra é uma decisão a defender.

---

## 7.8. O que NÃO entra no rateio

- **Vendas** — preço de venda é independente do custo.
- **Apropriações sem regra aplicável** — se uma apropriação cai numa folha sem regra e a regra geral foi desativada (raro), o valor fica fora do rateio. O sistema **não joga erro** — apenas ignora.
- **Custos lançados em obras diferentes** — o rateio é por obra; não há rateio cruzado entre obras.

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Apto X recebe mais que deveria | Fração ideal cadastrada errada | Cheque a fração; soma deve dar 1,0 |
| Apto Y recebe R$ 0 | Sem fração ideal (= 0) | Atualize a unidade |
| Total de custos por unidade ≠ total da obra | Diferença minúscula = arredondamento (esperado) | Diferença grande = regra de rateio não cobrindo todas as apropriações |
| Mudei regra mas relatório não atualizou | Cache desatualizado | Clique em **Recalcular rateio** |
| Regra `customizado` parou de funcionar | Removi uma unidade que tinha peso | Recadastre a unidade ou ajuste a regra |
| Rateio bizarro depois de adicionar unidade nova | Soma de frações ficou > 1,0 | Ajuste frações para fechar em 1,0 |

---

**Próximo passo:** [Capítulo 8 — Análise](08-analise.md), onde você vê o resultado de tudo isso em três relatórios financeiros.
