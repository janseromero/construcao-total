# 5. Orçamento

O orçamento é o **plano financeiro** da obra. Ele combina EAP + catálogo para dizer "quanto vou gastar em cada etapa". É contra ele que o sistema vai comparar tudo que for executado.

---

## 5.1. Conceitos

### Versionamento

Toda obra pode ter **vários orçamentos**, mas só um **aprovado** por vez:

- **Rascunho** — você está editando. Pode adicionar/remover itens.
- **Aprovado** — virou a referência ativa. Não dá mais pra editar itens.
- **Superado** — era aprovado, mas foi substituído por uma nova versão aprovada.

⚠️ Aprovar um orçamento novo **automaticamente marca o anterior como superado**. A transição é atômica — em nenhum instante existem dois orçamentos aprovados ao mesmo tempo.

### Itens

Cada item do orçamento tem:
- **EAP** — em qual folha da árvore ele é classificado (obrigatório).
- **Composição (opcional)** — receita pronta do catálogo.
- **Descrição** — texto livre ou copiado da composição.
- **Unidade** — `m²`, `m³`, `vb`, etc.
- **Quantidade** — quantas unidades.
- **Custo unitário** — R$ por unidade.
- **Custo total** — calculado: `quantidade × custo_unitario`.

O **total do orçamento** é a soma de todos os custos totais.

---

## 5.2. Quando criar um novo orçamento

Cenários comuns:

| Situação | Ação |
|----------|------|
| Início do projeto | Crie **Orçamento base v1** |
| Mudança grande de escopo (cliente mudou o projeto) | Crie **Revisão pós-projeto v2** |
| Imprevisto grande durante a obra (fundação foi muito pior que esperado) | Crie **Revisão pós-fundação v3** |
| Erro pequeno num item | Não crie nova versão — apenas anote no orçado×realizado |

Não tenha medo de versionar. Cada versão é uma foto de quanto você esperava gastar **naquele momento**. Comparar v1 com v3 mostra o quão longe a obra foi do plano original.

---

## 5.3. Criar o primeiro orçamento

1. Entre na obra → aba **Orçamento**.
2. **Novo orçamento**.
3. **Nome** — sugestão: `Orçamento base`. Status sai como `rascunho`.
4. **Criar**.

Na lista de orçamentos aparece sua **v1** em rascunho. Clique em **Editar itens** para abrir o editor.

---

## 5.4. Adicionar itens

No editor de orçamento:

1. Selecione a **EAP** (folha) — só folhas válidas aparecem.
2. **Unidade** — ex.: `m²`, `m³`, `un`, `vb`.
3. **Descrição** — descreva o que está orçando.
4. **Quantidade** — número decimal.
5. **Custo unitário (R$)** — preço por unidade.
6. **Adicionar item**.

O item aparece na tabela. O **custo total da obra** (no painel topo direito) atualiza automaticamente.

💡 Repita para todas as etapas significativas. Não precisa ter um item por insumo — quanto mais alto o nível, mais rápido você orça (sacrificando precisão).

### Exemplo — Residencial Aurora, primeira leva de itens

| EAP | Descrição | Un | Qtd | Custo unit. (R$) | Custo total (R$) |
|-----|-----------|-----|------|--------------------|--------------------|
| 1.1 Tapume | Tapume madeirite + porta | m | 60 | 90,00 | 5.400,00 |
| 1.4 Sondagem | SPT 6 furos | vb | 1 | 4.500,00 | 4.500,00 |
| 2.4 Concreto | Concreto fck 25 MPa | m³ | 18 | 480,00 | 8.640,00 |
| 2.3 Armação | Vergalhão CA-50 montado | kg | 1.800 | 12,00 | 21.600,00 |
| 3.1 Pilares | Estrutura de pilares (verba) | vb | 1 | 95.000,00 | 95.000,00 |
| 3.3 Lajes | Lajes maciças e nervuradas | m² | 1.040 | 220,00 | 228.800,00 |
| 4.1 Alvenaria | Alvenaria de vedação | m² | 1.800 | 98,88 | 177.984,00 |
| 6.2 Elétrica | Instalação elétrica completa | vb | 1 | 145.000,00 | 145.000,00 |
| 6.1 Hidráulica | Instalação hidráulica completa | vb | 1 | 88.000,00 | 88.000,00 |
| 8.4 Pisos | Piso porcelanato + assentamento | m² | 580 | 180,00 | 104.400,00 |
| 9.2 Pintura | Pintura interna duas demãos | m² | 1.600 | 28,00 | 44.800,00 |
| 9.3 Pintura externa | Textura acrílica + pintura | m² | 850 | 42,00 | 35.700,00 |
| 12.1 Engenharia | Engenharia e administração (12 meses) | vb | 1 | 60.000,00 | 60.000,00 |
| 12.2 Taxas | Alvará, ART, ISS, licenças | vb | 1 | 22.000,00 | 22.000,00 |
| **Total parcial** | | | | | **R$ 1.041.824,00** |

⚠️ Esta é uma versão simplificada. Um orçamento real de obra residencial deste porte tem 80–200 itens.

---

## 5.5. Remover itens

Na linha do item, clique em **Remover**. Total do orçamento recalcula.

⚠️ Só rascunhos aceitam edição. Orçamento aprovado é imutável — para corrigir, crie uma nova versão.

---

## 5.6. Aprovar o orçamento

Quando estiver satisfeito com a v1:

1. Volte para a lista de orçamentos da obra.
2. Na linha do orçamento, clique em **Aprovar**.
3. Confirme. Status muda para `aprovado`. Data e usuário de aprovação ficam registrados.

⚠️ Aprovar **só pode ser feito pelo Proprietário**. Operacional vê o orçamento, mas não pode aprovar.

A partir daqui:
- Os itens deste orçamento viram a **referência** do comparativo **orçado × realizado**.
- Você não pode mais editar nem remover itens deste orçamento.
- Para corrigir/atualizar, **crie uma nova versão** (será v2).

---

## 5.7. Criar uma revisão (v2, v3...)

1. Aba **Orçamento** → **Novo orçamento**.
2. Nome — sugestão: `Revisão 1 — pós-fundação` (ou o motivo da revisão).
3. **Criar**. Nasce como v2 em rascunho.
4. Edite itens, ajuste valores.
5. Quando aprovar, a v1 vira `superado` automaticamente e a v2 vira a referência ativa.

💡 No MVP, **a v2 não copia itens da v1**. Você precisa relançar. Na Onda 2 isso vira "duplicar versão".

---

## 5.8. Boas práticas

1. **Versão base sempre cedo**, mesmo incompleta. Antes de a obra começar, já tenha uma v1 aprovada — é a única forma de o sistema medir desvios.
2. **Comente o motivo** das revisões no campo "nome" (`Revisão 2 — aumento do preço do aço`).
3. **Não ultrapasse 3–5 versões.** Se está revisando direto, seu plano está mal feito — recue, replaneje.
4. **Inclua reservas/contingência** como item explícito (`12.5 Contingência — 5% do total`).
5. **Custos indiretos não esquecer** (ART, alvarás, engenharia, taxa do contador, IPTU da obra...). Sem eles, sua margem por unidade vai parecer maior do que é.

---

## 5.9. Visão consolidada do orçamento

Por enquanto, a visão consolidada (total por etapa raiz, % do total, custo por m²) é exibida na seção **Análise → Orçado × Realizado** depois que o orçamento for aprovado.

A tela dedicada de "visão consolidada do orçamento com export PDF/Excel" entra na Onda 2.

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Não consigo aprovar | Está logado como Operacional | Peça ao Proprietário aprovar |
| Não consigo editar item | Orçamento já está aprovado | Crie nova versão |
| Não consigo remover orçamento | Já foi aprovado | Não dá pra remover aprovado; crie revisão e aprove |
| Total não atualiza | Ainda nada — pode atualizar a página | Reload soluciona |
| Item duplicado | Cliquei "Adicionar" duas vezes | Remova o duplicado |
| EAP não aparece na lista | Você apontou para um nó intermediário antes de criar filhos | Refaça a EAP (vide cap. 3) |

---

**Próximo passo:** [Capítulo 6 — Execução](06-execucao.md), onde a obra começa de fato e você lança o que está sendo gasto.
