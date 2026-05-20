# 4. Catálogo

O catálogo é o **dicionário** do seu sistema. Antes de orçar ou lançar nota, você precisa cadastrar:

- **Fornecedores** — quem vende para você (material, serviço, equipamento).
- **Insumos** — o que entra na obra (material, mão de obra, equipamento).
- **Composições** — receitas que combinam insumos em serviços ("1 m² de alvenaria = X tijolos + Y horas de pedreiro").

---

## 4.1. Fornecedores

### 4.1.1. O que é

Fornecedor é qualquer pessoa física ou jurídica que entrega algo à obra. Pode ser:

- **Material** — depósito de construção, fábrica de cimento.
- **Serviço** — empreiteiro de pintura, encanador, engenheiro autônomo.
- **Equipamento** — locadora de andaime, betoneira.
- **Misto** — empresa que entrega material e instala (ex.: gesso acartonado).

### 4.1.2. Como cadastrar

1. Menu lateral → **Fornecedores**.
2. **Novo fornecedor**.
3. Preencha:
   - **Nome** — razão social ou nome fantasia. Obrigatório.
   - **CNPJ/CPF** — opcional. Recomendado para vincular NFs.
   - **Tipo** — material / serviço / equipamento / misto.
   - **Contato** — telefone, e-mail, nome da pessoa responsável.
4. **Salvar**.

### 4.1.3. Exemplo — Residencial Aurora

| Nome | CNPJ | Tipo | Contato |
|------|------|------|---------|
| Concretex Concreto SP Ltda | 11.222.333/0001-44 | material | (11) 4002-8922 / João Silva |
| Pedreirão Mão de Obra ME | 22.333.444/0001-55 | servico | (11) 99876-5432 / Mestre Pedro |
| Locadora ABC Andaimes | 33.444.555/0001-66 | equipamento | locacao@abc.com.br |
| Casa Forte Materiais | 44.555.666/0001-77 | material | (11) 3344-5566 |
| Eng. Maria Santos (autônoma) | 555.666.777-88 | servico | maria@santosengenharia.com.br |

⚠️ Quando você lança uma NF, o sistema pede o fornecedor. **Cadastre antes** — não dá pra criar fornecedor no meio do fluxo de NF (no MVP).

### 4.1.4. Editar e remover

- **Remover** — só se não houver NF nem contrato ligado. Caso contrário, o sistema bloqueia.

---

## 4.2. Insumos

### 4.2.1. O que é

Insumo é a **unidade atômica de custo** da sua obra. Três tipos:

| Tipo | Exemplos | Unidade típica |
|------|----------|----------------|
| **Material** | Cimento, areia, brita, tijolo, tubo PVC | kg, m³, un, m |
| **Mão de obra** | Pedreiro, servente, eletricista, engenheiro | h (hora), d (diária) |
| **Equipamento** | Betoneira, andaime, caminhão | h (hora), d (diária), vb (verba) |

### 4.2.2. Por que cadastrar insumos

- **Reaproveitamento:** uma vez cadastrado, você usa em N composições e N apontamentos.
- **Atualização de preço centralizada:** mudou o preço do cimento? Atualiza o insumo, e as composições novas usam o preço novo automaticamente.
- **Vínculo opcional com SINAPI:** você pode amarrar seu insumo a um código SINAPI. Quando o importer SINAPI da Onda 2 chegar, os preços virão automaticamente.

⚠️ **Snapshots, não referências:** quando um insumo entra numa composição ou num apontamento, o preço daquele momento é gravado (snapshot). Mudar o preço do insumo depois **não altera** lançamentos antigos. Isso é proposital para manter a história fiel.

### 4.2.3. Como cadastrar

1. Menu lateral → **Insumos**.
2. **Novo insumo**.
3. Preencha:
   - **Código** — código interno, único por construtora. Ex.: `MAT-CIM-CP2`, `MO-PED`, `EQ-AND`.
   - **Tipo** — material / mão de obra / equipamento.
   - **Descrição** — `Cimento CP-II 50kg`, `Pedreiro`, `Andaime tubular`.
   - **Unidade** — abreviação. Ex.: `kg`, `h`, `m³`.
   - **Código SINAPI** — opcional. Use o código oficial se conhecer (ex.: `1532` para cimento CP-II).
   - **Custo unitário ref.** — preço de referência em R$. Ex.: `45,00` para o saco de cimento.
4. **Salvar**.

### 4.2.4. Convenção de códigos sugerida

Use prefixos para organizar:

| Prefixo | Significado |
|---------|-------------|
| `MAT-` | Material |
| `MO-` | Mão de obra |
| `EQ-` | Equipamento |

Exemplos:
- `MAT-CIM-CP2` — cimento CP-II.
- `MAT-AREIA-MED` — areia média.
- `MAT-BLOCO-19` — bloco cerâmico 19 cm.
- `MO-PED` — pedreiro.
- `MO-SER` — servente.
- `MO-ELE` — eletricista.
- `EQ-BET-400L` — betoneira 400 litros.

### 4.2.5. Exemplo — Residencial Aurora

| Código | Descrição | Un | Tipo | Custo ref. (R$) |
|--------|-----------|----|------|------------------|
| MAT-CIM-CP2 | Cimento CP-II 50kg | sc | material | 45,00 |
| MAT-AREIA-MED | Areia média | m³ | material | 110,00 |
| MAT-BRITA-1 | Brita 1 | m³ | material | 135,00 |
| MAT-BLOCO-19 | Bloco cerâmico 9x19x29 | un | material | 2,80 |
| MAT-VERG-CA50-10 | Vergalhão CA-50 ⌀10mm | kg | material | 8,50 |
| MAT-TUBO-PVC-100 | Tubo PVC 100mm 6m | un | material | 78,00 |
| MO-ENG | Engenheiro civil | h | mao_obra | 250,00 |
| MO-MEST | Mestre de obras | h | mao_obra | 80,00 |
| MO-PED | Pedreiro | h | mao_obra | 35,00 |
| MO-SER | Servente | h | mao_obra | 22,00 |
| MO-ELE | Eletricista | h | mao_obra | 45,00 |
| MO-ENC | Encanador | h | mao_obra | 45,00 |
| MO-PIN | Pintor | h | mao_obra | 30,00 |
| EQ-BET-400L | Betoneira 400 litros | h | equipamento | 18,00 |
| EQ-AND-TUB | Andaime tubular | m²·dia | equipamento | 5,50 |

---

## 4.3. Composições

### 4.3.1. O que é

Composição é uma **receita**: define quantos insumos entram em uma unidade de serviço.

Exemplo: **"1 m² de alvenaria de vedação 9 cm"** consome:
- 13 blocos
- 0,008 m³ de areia
- 8 kg de cimento (para argamassa)
- 0,8 h de pedreiro
- 1,2 h de servente

O **custo unitário da composição** é a soma de `insumo × coeficiente × custo unitário` de cada linha.

### 4.3.2. Para que serve

- **Orçar mais rápido:** em vez de listar cada material por etapa, você diz "300 m² de alvenaria" e o sistema multiplica.
- **Padronizar:** sua composição de alvenaria fica igual em todas as obras.
- **Migração para SINAPI:** quando o importer SINAPI chegar, você pode adotar composições oficiais como referência.

### 4.3.3. Como cadastrar (via API no MVP)

A tela de composições entra na Onda 2. No MVP, cadastre via API:

```bash
POST /composicoes
{
  "codigo": "ALV-VED-9",
  "descricao": "Alvenaria de vedação com bloco cerâmico 9 cm",
  "unidade": "m²",
  "sinapi_codigo": "87504",
  "insumos": [
    {"insumo_id": "<id MAT-BLOCO-19>", "coeficiente": 13},
    {"insumo_id": "<id MAT-AREIA-MED>", "coeficiente": 0.008},
    {"insumo_id": "<id MAT-CIM-CP2>", "coeficiente": 0.16},
    {"insumo_id": "<id MO-PED>", "coeficiente": 0.8},
    {"insumo_id": "<id MO-SER>", "coeficiente": 1.2}
  ]
}
```

O sistema calcula automaticamente:
```
custo_unitario_calculado = sum(coeficiente × custo_unitario_snapshot)
= 13×2,80 + 0,008×110 + 0,16×45 + 0,8×35 + 1,2×22
= 36,40 + 0,88 + 7,20 + 28,00 + 26,40
= R$ 98,88 por m² de alvenaria
```

⚠️ Composição é **opcional** no MVP. Você pode orçar item por item digitando descrição livre e custo unitário direto.

---

## 4.4. Quanto investir em catálogo no início?

Não tente cadastrar tudo de uma vez. Comece **enxuto**:

| Quando | Cadastrar |
|--------|-----------|
| **Antes de orçar** | 10–20 insumos principais (cimento, areia, brita, blocos, ferro, pedreiro, servente, mestre) |
| **Antes de lançar a 1ª NF** | Fornecedor da NF |
| **Conforme NFs aparecem** | Novos fornecedores e insumos que você ainda não tem |

Depois de 2–3 meses, seu catálogo está consolidado.

💡 Quando o importer SINAPI da Onda 2 estiver pronto, você vai poder **importar centenas de insumos de uma vez** com preços atualizados da CAIXA (por estado).

---

## Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| "Insumo não encontrado" ao salvar composição | UUID errado | Confira o ID via `GET /insumos` |
| Preço de composição desatualizado | Snapshots não recalculam automaticamente | Edite a composição — ao salvar, snapshots são refeitos do insumo |
| Não consigo apagar insumo | Está em composição ou apontamento | Remova vínculos primeiro |
| Não consigo apagar fornecedor | Tem NF ligada | Não remova; marque o fornecedor inativo (Onda 2) |
| Códigos duplicados | Sistema bloqueia | Use prefixos (`MAT-`, `MO-`, `EQ-`) |

---

**Próximo passo:** [Capítulo 5 — Orçamento](05-orcamento.md), onde você usa tudo que cadastrou aqui pra montar o plano financeiro da obra.
