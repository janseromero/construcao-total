# 6. Execução

Aqui a obra começa pra valer. Você vai lançar **tudo que está sendo gasto**, classificar cada gasto na EAP correta (apropriação) e o sistema vai começar a calcular o custo real da obra.

O módulo Execução tem 4 tipos de lançamento:

1. **Nota fiscal** — material e serviço com NF emitida.
2. **Apropriação** — ato de dizer "este valor pertence a esta etapa da EAP".
3. **Apontamento de mão de obra** — horas trabalhadas pela equipe própria.
4. **Lançamento manual** — custos sem NF (taxas, emolumentos).

---

## 6.1. Notas fiscais

### 6.1.1. Lançar uma NF manualmente

1. Entre na obra → aba **Execução**.
2. **Nova NF**.
3. Preencha:
   - **Fornecedor** — escolha da lista (cadastre antes em Fornecedores).
   - **Número** — número da NF.
   - **Data emissão** — data do documento.
   - **Valor total (R$)** — valor total da nota.
   - **Descrição do item** — descrição que aparecerá no item único da NF (no MVP, cada NF tem 1 item; lançar com múltiplos itens via API).
4. **Salvar NF**.

A NF aparece na tabela com status **pendente_apropriacao**.

⚠️ No MVP, o formulário cria uma NF com **1 item** = valor total. Se a NF real tem múltiplos produtos/serviços, lance-os via API ou aguarde a tela completa de Onda 2:

```bash
POST /notas-fiscais
{
  "obra_id": "...",
  "fornecedor_id": "...",
  "numero": "12345",
  "data_emissao": "2026-04-15",
  "valor_total": "8400.00",
  "itens": [
    {"descricao": "Cimento CP-II", "unidade": "sc", "quantidade": "100", "valor_unitario": "45", "valor_total": "4500"},
    {"descricao": "Areia média", "unidade": "m³", "quantidade": "20", "valor_unitario": "110", "valor_total": "2200"},
    {"descricao": "Frete", "unidade": "vb", "quantidade": "1", "valor_unitario": "1700", "valor_total": "1700"}
  ]
}
```

### 6.1.2. Importar XML NF-e (Onda 2)

A Onda 2 do MVP vai aceitar upload do XML padrão da SEFAZ. O sistema extrai automaticamente fornecedor, número, itens, NCM, valores. Por enquanto, lançamento manual.

### 6.1.3. Status de uma NF

| Status | Significado |
|--------|-------------|
| **pendente_apropriacao** | Nenhum item apropriado ainda |
| **parcialmente_apropriada** | Pelo menos um item apropriado, mas nem todos totalmente |
| **totalmente_apropriada** | Todos os itens foram 100% apropriados |
| **cancelada** | NF cancelada (vai exigir estornos antes — Onda 2) |

O status muda automaticamente conforme você apropria.

---

## 6.2. Apropriação — o ato central do sistema

### 6.2.1. O que é apropriação

Apropriar é **classificar um valor em uma folha da EAP**. É a operação mais importante do dia a dia da execução.

Sem apropriar, o valor fica solto: você sabe que gastou R$ 8.400 com Concretex, mas não sabe se foi em Fundação, Estrutura, Laje, Piso...

Com apropriação, você diz: "destes R$ 8.400, R$ 6.000 vão para `2.4 Concreto da Fundação` e R$ 2.400 vão para `3.3 Lajes`".

### 6.2.2. Como apropriar um item de NF

1. Na tabela de NFs, ao lado do item, clique em **Apropriar**.
2. Abre um modal:
   - **Valor do item** — mostrado no topo do modal.
   - **EAP** — escolha a folha onde apropriar.
   - **Valor a apropriar (R$)** — pode ser o valor total ou uma parte.
3. **Apropriar**.

A apropriação é registrada. Se ainda sobrar valor não apropriado, clique em **Apropriar** de novo para a parte restante (em outra EAP).

### 6.2.3. Apropriar 100% em uma única EAP

Caso comum: NF de cimento que toda vai para uma etapa. Preencha o valor igual ao do item e selecione a EAP. Pronto.

### 6.2.4. Apropriar em múltiplas EAPs (split)

Caso comum: NF de concreto que vai parte pra fundação, parte pra estrutura.

Exemplo prático: NF de R$ 8.400 da Concretex (item único de R$ 8.400):

1. **Apropriar** → EAP `2.4 Concreto`, valor R$ 6.000 → confirma.
2. **Apropriar** novamente (o sistema permite, pois ainda sobra R$ 2.400) → EAP `3.3 Lajes`, valor R$ 2.400 → confirma.

Status da NF muda para **totalmente_apropriada**.

### 6.2.5. Regras de validação

⚠️ O sistema **bloqueia** apropriações que excedem o valor do item. Se o item é R$ 8.400 e você já apropriou R$ 6.000, a próxima apropriação não pode passar de R$ 2.400.

Mensagem de erro:
```
Apropriação excede valor do item NF
(já apropriado R$ 6000.00, novo R$ 5000.00, item R$ 8400.00)
```

### 6.2.6. Corrigir uma apropriação errada

⚠️ Apropriação **não pode ser editada**. Para corrigir:

1. **Remover** a apropriação errada (botão **Remover** ao lado dela).
2. Criar uma nova apropriação correta.

Isso é proposital — mantém o histórico fiel. Em Onda 2, vai existir "lançamento de estorno" mais explícito.

---

## 6.3. Apontamento de mão de obra

### 6.3.1. O que é

Quando você tem **equipe própria** (não empreiteiro), precisa lançar as **horas trabalhadas** de cada pessoa. Isso vira custo, e é classificado direto na EAP onde aquele dia o pedreiro estava trabalhando.

### 6.3.2. Quem lança

Geralmente o **Operacional** (engenheiro de obra, mestre, administrativo). É o tipo de lançamento mais frequente — diário ou semanal.

### 6.3.3. Como apontar

1. Aba **Execução** (no MVP, use a API ou aguarde tela dedicada).

```bash
POST /apontamentos
{
  "obra_id": "...",
  "eap_id": "<id de 4.1 Alvenaria>",
  "data": "2026-04-20",
  "insumo_id": "<id de MO-PED>",
  "quantidade": "8",
  "observacao": "Pedreiro João — execução parede divisória apto 201"
}
```

O sistema:
- Pega o `custo_unitario_referencia` do insumo (snapshot do momento).
- Calcula `valor_total = quantidade × custo_unitario`.
- Cria automaticamente a apropriação na EAP escolhida.

### 6.3.4. Visibilidade

⚠️ Quando o **Operacional** vê seus próprios apontamentos, o **valor em R$ não aparece** — só a quantidade. O Proprietário vê tudo.

Exemplo:
- Operacional vê: `20/04/2026 — Alvenaria — Pedreiro — 8 horas — (valor oculto)`
- Proprietário vê: `20/04/2026 — Alvenaria — Pedreiro — 8 horas — R$ 280,00`

### 6.3.5. Apontamento como insumo

Cada apontamento exige escolher um **insumo de tipo mão_obra** (Pedreiro, Servente, etc). Por isso é importante cadastrar esses insumos antes (cap. 4) com o custo unitário correto (custo da hora, incluindo encargos).

💡 **Dica para o custo da hora:** salário mensal + encargos (~80% no Brasil) ÷ 176 horas/mês ÷ produtividade.

---

## 6.4. Lançamento manual de custo

### 6.4.1. O que é

Custos que não têm NF nem apontamento de funcionário — taxas, emolumentos, alvarás, transferências, multas, contas avulsas.

### 6.4.2. Quem lança

⚠️ **Apenas o Proprietário** pode fazer lançamentos manuais. Operacional não vê esta opção.

### 6.4.3. Como lançar (via API no MVP)

```bash
POST /lancamentos-manuais
{
  "obra_id": "...",
  "eap_id": "<id de 12.2 Taxas>",
  "data": "2026-04-10",
  "valor": "850.00",
  "descricao": "Taxa de alvará de construção — Prefeitura",
  "fornecedor_id": null
}
```

O sistema cria automaticamente a apropriação. O lançamento aparece no orçado × realizado e no rateio.

---

## 6.5. Fluxo recomendado de execução

Mensalmente:

1. **Receba as NFs** (no MVP, conferir com o contador o que chegou no mês).
2. **Lance cada NF** com seus itens.
3. **Apropie cada item** na EAP correta. Não deixe para depois — vai esquecer.
4. **Aponte mão de obra** (a equipe operacional deve fazer isso diariamente ou semanalmente).
5. **Lance custos avulsos** (taxas, alvarás, contador).
6. **Revise Análise → orçado × realizado** para ver se alguma etapa está estourando.

---

## 6.6. NF que cobre múltiplos meses

Caso comum: fatura de eletricidade da obra de janeiro chega em fevereiro.

- **Data emissão** — data real da NF (fevereiro).
- **Data competência da apropriação** — você pode escolher janeiro (o competente).

Isso garante que a curva S e o orçado×realizado reflitam o mês onde o custo *foi gerado*, não onde foi pago.

⚠️ No MVP, a "data de competência" é setada na apropriação, não na NF. Você pode usá-la para corrigir desfases.

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| "Apropriação excede valor do item" | Tentando apropriar mais que o item permite | Reduza o valor ou cheque apropriações já feitas |
| NF fica em `pendente_apropriacao` para sempre | Esqueci de apropriar | Volte e apropie |
| Apontamento sem custo | Insumo de mão de obra sem custo unitário cadastrado | Edite o insumo e ponha o valor |
| "Não tenho NF, é em dinheiro" | Use lançamento manual | Vide §6.4 |
| Fornecedor não aparece na lista da NF | Não cadastrou ainda | Cadastre em Fornecedores |
| Operacional viu valor em R$ que não deveria | É bug — reporte | Sistema bloqueia, mas se vazou avise |
| Apropriação ficou na EAP errada | Não dá pra editar | Remova e refaça |

---

**Próximo passo:** [Capítulo 7 — Rateio](07-rateio.md), onde você entende como o sistema distribui o custo apropriado entre os apartamentos.
