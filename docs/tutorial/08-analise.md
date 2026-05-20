# 8. Análise

Aqui mora o **valor real do produto**. Os três relatórios desta aba são o que diferencia o Construtor Total de uma planilha.

A aba **Análise** tem:

1. **Custo por unidade** — quanto cada apartamento custou até agora (visível para todos).
2. **Margem por unidade** — preço de venda menos custo (visível apenas para Proprietário).
3. **Orçado × realizado** — comparativo do plano contra a realidade.

E no canto da tela tem o **resumo executivo** (VGV, custo total, margem total), visível apenas no painel Visão geral, restrito ao Proprietário.

---

## 8.1. Custo por unidade

### O que mostra

Cada linha é uma unidade. Colunas:

| Coluna | Significado |
|--------|-------------|
| Unidade | Identificador (Apto 101, 201, etc) |
| Área (m²) | Área privativa cadastrada |
| Fração ideal | Fração ideal cadastrada |
| Custo acumulado (R$) | Soma de todas as quotas que o rateio atribuiu a essa unidade |
| Custo / m² | Custo acumulado ÷ área privativa |

### Para que serve

- Saber em tempo real **quanto cada apartamento está custando**.
- Identificar **diferença entre tipologias** — coberturas naturalmente custam mais por m² que térreos.
- Detectar **erros de cadastro** — se um apartamento de 60 m² está custando o dobro de um igual ao lado, algo está errado (provavelmente fração ideal ou área).

### Quando consultar

- **Toda semana** durante a execução, pra acompanhar evolução.
- **Antes de tabelar preços** — você tem ideia do custo já comprometido.
- **No fechamento** — número final para análise de rentabilidade.

### Quem vê

✅ Proprietário e Operacional.

⚠️ Para o Operacional, este relatório é o **único** que mostra valores monetários por unidade (sem margem, sem preço de venda). Ainda assim, considere se isso é alinhado com a cultura da construtora.

---

## 8.2. Margem por unidade

### O que mostra

| Coluna | Significado |
|--------|-------------|
| Unidade | Identificador |
| Custo | Custo acumulado (do relatório anterior) |
| Preço de venda | Preço final da venda (ou preço tabela se ainda não vendida) |
| Margem (R$) | Preço de venda − custo |
| Margem (%) | Margem ÷ preço de venda × 100 |

### Para que serve

- **O número que move uma construtora.** Quanto cada apartamento está dando de lucro.
- **Detectar vendas problemáticas:** se o apto 102 foi vendido por R$ 480.000 mas custou R$ 470.000, a margem de R$ 10.000 talvez não compense.
- **Apoiar decisão de preço** dos apartamentos ainda não vendidos: olhar quanto os já vendidos estão dando.
- **Renegociação:** se a margem real está muito alta numa unidade reservada mas ainda não escriturada, talvez você consiga conceder desconto.

### Estados possíveis

| Cenário | Coluna preço | Coluna margem |
|---------|--------------|---------------|
| Unidade sem venda nem reserva | — | — |
| Unidade reservada | Preço da reserva | Calculado |
| Unidade vendida | Preço final | Calculado |
| Unidade distratada | — | — (volta a ser disponível) |

### Quem vê

✅ Apenas Proprietário. Operacional vê apenas uma mensagem: "Visível apenas para o perfil Proprietário".

⚠️ Este bloqueio é **forçado no servidor**, não só no front. Mesmo que alguém tente acessar o endpoint diretamente, vem `403 Forbidden`.

---

## 8.3. Orçado × Realizado

### O que mostra

Tabela com uma linha por **etapa raiz** da EAP (níveis 1 — Serviços Preliminares, 2 — Fundação, etc).

| Coluna | Significado |
|--------|-------------|
| Etapa | Código + nome da raiz |
| Orçado | Soma de itens do orçamento aprovado na sub-árvore |
| Realizado | Soma de apropriações na sub-árvore |
| Δ | Realizado − Orçado |
| % | Realizado ÷ Orçado × 100 |

### Como ler

| % | Interpretação |
|---|---------------|
| < 100% | Etapa **abaixo** do orçado — bom |
| ≈ 100% | Etapa no plano |
| > 100% | Etapa **estourou** — investigue |
| 0% | Nada realizado ainda — pode ser que a etapa ainda não começou |

A coluna **Δ** vem destacada (cor de alerta) quando positiva — sinal visual de estouro.

### Para que serve

- **Monitoramento mensal** do quanto a obra está fugindo do plano.
- **Sinalizar problemas cedo**: se a fundação já estourou em 30% e a estrutura nem começou, a obra inteira vai sofrer.
- **Justificar revisões de orçamento**: se uma etapa estourou de forma estrutural, talvez seja hora de uma v2.

### Quem vê

✅ Proprietário e Operacional (sem coluna de margem ou venda, apenas custos).

⚠️ Só funciona com **orçamento aprovado**. Se nenhuma versão do orçamento foi aprovada, a tabela aparece vazia.

---

## 8.4. Resumo executivo (Visão geral)

Na aba **Visão geral** da obra, o Proprietário vê um painel com:

| Métrica | Significado |
|---------|-------------|
| VGV | Valor Geral de Vendas — soma dos preços de venda (efetivos ou tabela) |
| Custo total | Soma de todos os custos acumulados |
| Margem total | VGV − custo total |
| Margem % | Margem ÷ VGV × 100 |
| Unidades vendidas | Contagem de unidades em venda/reserva |

Para o Operacional, este painel é substituído por "Resumo financeiro disponível apenas para o perfil Proprietário".

---

## 8.5. Como atualizar / recalcular

Os relatórios usam um **cache materializado** do rateio. Em três situações o cache é refeito:

1. **Automático ao abrir Custo por unidade.**
2. **Manual** — botão **Recalcular rateio** no topo da aba Análise.
3. **Em uma migração futura** (Onda 2): após cada apropriação, recalcular em job assíncrono.

Se mudou regras de rateio ou alguma fração ideal, **clique em Recalcular**.

---

## 8.6. Exports (Onda 2)

Export para PDF e Excel dos três relatórios entra na Onda 2. Por enquanto, copie da tela ou use a API:

```bash
GET /obras/{id}/analise/custo-por-unidade
GET /obras/{id}/analise/margem-por-unidade
GET /obras/{id}/analise/orcado-vs-realizado
GET /obras/{id}/analise/resumo
```

Todas retornam JSON.

---

## 8.7. Como agir com cada relatório

| Relatório | Decisão que ele apoia |
|-----------|----------------------|
| Custo por unidade | Tabelar preço de novas unidades; aceitar/recusar proposta de desconto; identificar tipologia mais rentável |
| Margem por unidade | Avaliar performance comercial da obra; preparar fechamento financeiro; comparar margem real vs. esperada por tipologia |
| Orçado × Realizado | Decidir nova versão de orçamento; sinalizar problema operacional; renegociar com fornecedor; entender se cronograma vai estourar (atraso = custo indireto extra) |
| Resumo executivo | Apresentação para sócios e bancos; decisão sobre próximas obras (replicar ou ajustar formato) |

---

## 8.8. Limitações conhecidas no MVP

- **Não há análise por período** — todos os relatórios são "até agora". A linha temporal (curva S realizada × prevista) entra na Onda 2.
- **Não há comparativo entre obras** — relatórios são sempre dentro de uma obra.
- **Não há análise por tipologia** — relatórios são por unidade individual.
- **Não há audit log na UI** — mas os eventos são gravados no banco.

Tudo isso evolui nas próximas ondas.

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Custo por unidade dá zero | Nada apropriado ainda, ou fração ideal = 0 | Lance apropriações ou ajuste frações |
| Custo total ≠ soma das unidades | Arredondamento (pequeno) ou falha de rateio | Recalcule; se persistir, abra ticket |
| Orçado × realizado vazio | Sem orçamento aprovado | Aprove um orçamento |
| Margem só tem `—` | Nenhuma venda registrada ainda | Registre vendas |
| Operacional vendo margem | Bug — reporte | Sistema bloqueia, mas reporte |
| Resumo executivo trava | Provavelmente sem unidades | Cadastre unidades |
| % > 100% em todas as etapas | Orçamento subestimado ou esquecido itens | Crie revisão |

---

**Próximo passo:** [Capítulo 9 — Vendas](09-vendas.md), o último módulo do MVP.
