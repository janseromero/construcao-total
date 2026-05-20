# Construtor Total — Modelo de Domínio

> Status: **draft v1** — base para implementação da Onda 1. Sujeito a refinamento conforme features evoluem.

Este documento descreve as entidades centrais do sistema, suas relações, invariantes e decisões de modelagem. É a fonte de verdade para o schema do banco e para a linguagem do produto (ubiquitous language).

---

## 1. Princípios de modelagem

1. **Multi-tenant por design.** Toda entidade de negócio carrega `tenant_id`. Nenhuma query pode rodar sem filtro de tenant — isso é regra de aplicação, reforçada por testes e (futuramente) Row Level Security no Postgres.
2. **Imutabilidade onde dói.** Lançamentos financeiros (NF, medição, venda) são *append-only* em produção: correção vira lançamento de estorno + novo lançamento, com `audit_log` registrando autor e motivo.
3. **Snapshot de custo no momento do lançamento.** Preço de insumo muda toda hora (SINAPI atualiza mensal, fornecedor reajusta). Lançamentos guardam o valor unitário do momento, nunca recalculam por lookup.
4. **Rateio é derivado.** Custo por unidade é sempre recalculado a partir dos lançamentos + regra de rateio vigente. Não armazenamos o resultado como "verdade", apenas como cache materializado (com timestamp de recálculo).
5. **EAP é hierárquica.** Estrutura Analítica do Projeto é a espinha dorsal: orçamento, apropriação, comparativo orçado×realizado, rateio — tudo pendura na EAP.
6. **Visibilidade financeira no backend.** O perfil Operacional não pode receber valores de venda nem margem em response payloads — filtro no serializer/route, não só no front.

---

## 2. Visão geral (mapa de contextos)

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Identidade     │    │    Catálogo      │    │   Referência     │
│  Tenant, User    │    │ Insumo, Composi- │    │  SINAPI Insumo,  │
│                  │    │ ção, Fornecedor  │    │  SINAPI Composi- │
└────────┬─────────┘    └────────┬─────────┘    │  ção (versionada)│
         │                       │              └────────┬─────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                          Obra (Empreendimento)                    │
│  Tipologia, Unidade, EAP, Cronograma, Contrato, RegraRateio       │
└────────┬───────────────────────────────────────────────┬─────────┘
         │                                               │
         ▼                                               ▼
┌──────────────────┐                          ┌──────────────────┐
│    Orçamento     │                          │    Execução      │
│ Orçamento (vers) │                          │ NF, NF Item,     │
│ Orçamento Item   │                          │ Apropriação,     │
│                  │                          │ Medição          │
└────────┬─────────┘                          └────────┬─────────┘
         │                                             │
         └──────────────────┬──────────────────────────┘
                            ▼
                  ┌──────────────────┐
                  │     Análise      │
                  │ Rateio Calculado │
                  │ Margem por Unid. │
                  └──────────────────┘

         ┌──────────────────┐
         │     Vendas       │
         │ Comprador, Venda │  → entra na Análise
         └──────────────────┘

         ┌──────────────────┐
         │   Transversal    │
         │   Audit Log      │
         └──────────────────┘
```

---

## 3. Entidades

Convenções:
- Todo registro tem `id` (UUID v4), `created_at`, `updated_at`.
- Toda entidade de negócio tem `tenant_id` (FK Tenant). Catálogos de referência (SINAPI) são globais (sem tenant).
- Campos monetários: `Numeric(18, 4)` em BRL. Quantidades: `Numeric(18, 6)`. Percentuais: `Numeric(7, 4)` (0–100, 4 casas).
- Soft delete via `deleted_at` apenas em entidades de cadastro (não em lançamentos financeiros).

### 3.1. Identidade

#### `tenant`
Construtora cliente do SaaS.
- `id`, `nome`, `cnpj` (único), `razao_social`, `plano` (enum: `free`, `pro` — placeholder), `ativo` (bool).

#### `user`
Usuário humano vinculado a um tenant.
- `id`, `tenant_id`, `email` (único por tenant), `nome`, `senha_hash`, `role` (enum: `proprietario`, `operacional`), `ativo`.
- Invariante: todo tenant tem pelo menos um `proprietario` ativo.

### 3.2. Catálogo (do tenant)

#### `fornecedor`
- `id`, `tenant_id`, `cnpj_cpf`, `nome`, `tipo` (enum: `material`, `servico`, `equipamento`, `misto`), `contato`, `observacoes`.

#### `insumo`
Material, mão de obra ou equipamento usado em composições e lançamentos.
- `id`, `tenant_id`, `codigo` (interno), `descricao`, `unidade` (m, m², m³, kg, h, vb, un, etc), `tipo` (enum: `material`, `mao_obra`, `equipamento`), `sinapi_insumo_id` (FK nullable — vinculação opcional à SINAPI), `custo_unitario_referencia` (snapshot, pode divergir da SINAPI).

#### `composicao`
Serviço composto por insumos (ex.: "Alvenaria de vedação 14cm com bloco cerâmico").
- `id`, `tenant_id`, `codigo`, `descricao`, `unidade`, `sinapi_composicao_id` (FK nullable), `custo_unitario_calculado` (cache, recalcula via trigger ou serviço).

#### `composicao_insumo`
- `composicao_id`, `insumo_id`, `coeficiente` (qtd de insumo por unidade da composição), `custo_unitario_snapshot`.

### 3.3. Referência SINAPI (global, sem tenant)

> Importada via pipeline mensal a partir do CSV da CAIXA. Versionada por mês de referência e UF (a SINAPI varia por estado).

#### `sinapi_insumo`
- `id`, `codigo`, `descricao`, `unidade`, `uf`, `mes_referencia` (date, dia 1), `preco_mediano`, `origem_desonerada` (bool).

#### `sinapi_composicao`
- `id`, `codigo`, `descricao`, `unidade`, `uf`, `mes_referencia`, `custo_total`.

#### `sinapi_composicao_insumo`
- `sinapi_composicao_id`, `sinapi_insumo_id` ou `sinapi_composicao_filho_id` (composição pode conter sub-composição), `coeficiente`.

**Decisão:** o catálogo do tenant (`insumo`, `composicao`) é independente; o vínculo com SINAPI é opcional e serve como "trazer dados de referência" e "atualizar preço". Construtora pode customizar.

### 3.4. Obra

#### `obra`
- `id`, `tenant_id`, `nome`, `endereco`, `data_inicio_prevista`, `data_fim_prevista`, `data_inicio_real` (nullable), `data_fim_real` (nullable), `area_total_construida` (m²), `area_terreno` (m²), `em_afetacao` (bool, default false — **gancho Q9**), `regime_tributario` (enum placeholder: `lucro_real`, `lucro_presumido`, `rep` — não usado no MVP), `status` (enum: `planejamento`, `em_obra`, `concluida`, `pausada`), `uf` (para resolver SINAPI).

#### `tipologia`
Tipo de apartamento (ex.: "Tipo A — 2 dormitórios — 60m²").
- `id`, `obra_id`, `nome`, `area_privativa_m2`, `area_comum_proporcional_m2`, `descricao`.

#### `unidade`
Apartamento físico.
- `id`, `obra_id`, `tipologia_id`, `identificador` (ex.: "Apto 101"), `andar`, `bloco` (nullable), `fracao_ideal` (Numeric 12,8 — soma de todas as unidades = 1.0), `area_privativa_m2` (snapshot da tipologia, editável por unidade).
- Invariante: `SUM(fracao_ideal)` por obra ≤ 1.0 (validado em commit; relatórios alertam se ≠ 1.0).

#### `eap` (Estrutura Analítica do Projeto)
Hierárquica. Define as etapas/serviços onde tudo é apropriado.
- `id`, `obra_id`, `parent_id` (nullable, self-reference), `codigo` (ex.: "1.2.3"), `nome`, `nivel` (int, derivado), `ordem` (int, para sort).
- Exemplo: `1 Serviços Preliminares` → `1.1 Tapume` → `1.1.1 Material` / `1.1.2 Mão de obra`.

#### `cronograma_etapa`
Liga uma folha da EAP a datas e % previstos.
- `id`, `obra_id`, `eap_id`, `data_inicio_prevista`, `data_fim_prevista`, `peso_financeiro_percentual`, `data_inicio_real` (nullable), `data_fim_real` (nullable), `percentual_concluido` (0–100).
- Usado para gerar a Curva S e medir avanço físico.

#### `contrato`
Contrato com empreiteiro/fornecedor de serviço.
- `id`, `obra_id`, `fornecedor_id`, `numero`, `objeto`, `valor_total`, `data_assinatura`, `data_inicio`, `data_fim_prevista`, `status` (enum: `vigente`, `concluido`, `rescindido`).

### 3.5. Orçamento (versionado)

#### `orcamento`
Cabeçalho versionado por obra.
- `id`, `obra_id`, `versao` (int, sequencial por obra), `nome` (ex.: "Orçamento base", "Revisão 1 — pós-fundação"), `status` (enum: `rascunho`, `aprovado`, `superado`), `data_aprovacao`, `aprovado_por_user_id`, `custo_total_calculado` (cache).
- Invariante: apenas **um** orçamento por obra com status `aprovado` por vez (o ativo).

#### `orcamento_item`
Linha do orçamento.
- `id`, `orcamento_id`, `eap_id` (folha da EAP), `composicao_id` (nullable — pode ser item livre), `descricao` (snapshot, caso composição mude), `unidade`, `quantidade`, `custo_unitario` (snapshot), `custo_total` (computed).

### 3.6. Execução

#### `nota_fiscal`
Cabeçalho.
- `id`, `tenant_id`, `obra_id` (nullable — NF pode ainda não estar apropriada), `fornecedor_id`, `numero`, `serie`, `chave_acesso` (44 dígitos NF-e — único quando informado), `data_emissao`, `valor_total`, `valor_produtos`, `valor_servicos`, `valor_impostos`, `xml_original` (text/blob — guarda o XML quando importado), `status` (enum: `pendente_apropriacao`, `parcialmente_apropriada`, `totalmente_apropriada`, `cancelada`).

#### `nota_fiscal_item`
Item da NF (linha do XML ou inserido manualmente).
- `id`, `nota_fiscal_id`, `descricao`, `ncm` (nullable), `unidade`, `quantidade`, `valor_unitario`, `valor_total`, `insumo_id` (nullable — vínculo opcional ao catálogo do tenant).

#### `apropriacao_custo`
**Coração da apropriação.** Liga um item de NF (ou parte dele) a uma folha da EAP.
- `id`, `tenant_id`, `obra_id`, `eap_id`, `origem_tipo` (enum: `nota_fiscal_item`, `medicao`, `lancamento_manual`, `apontamento_mao_obra`), `origem_id` (UUID polimórfico — o serviço de aplicação garante integridade), `valor` (Numeric 18,4 BRL), `quantidade` (nullable — pra mão de obra: horas), `data_competencia`, `descricao`, `created_by_user_id`.
- Permite **rateio fracionado**: uma NF de R$ 10.000 pode virar 2 apropriações (R$ 7.000 em "fundação", R$ 3.000 em "estrutura").
- Não tem `updated_at` lógico: corrigir = criar apropriação de estorno (valor negativo) + nova apropriação.

#### `medicao`
Medição de contrato de empreiteiro.
- `id`, `tenant_id`, `contrato_id`, `obra_id`, `numero` (sequencial por contrato), `data_competencia`, `percentual_periodo`, `valor_periodo`, `descricao`, `status` (enum: `pendente`, `aprovada`, `paga`).
- Ao aprovar, gera `apropriacao_custo` automática para a(s) EAP(s) do contrato.

#### `apontamento_mao_obra`
Lançamento de horas / dias trabalhados (perfil Operacional).
- `id`, `tenant_id`, `obra_id`, `eap_id`, `data`, `insumo_id` (mão de obra), `quantidade` (horas), `custo_unitario_snapshot` (do insumo), `valor_total` (computed).
- Gera `apropriacao_custo` ao ser salvo.

### 3.7. Rateio

#### `regra_rateio`
Regra de como o custo de uma EAP (ou da obra inteira) é distribuído entre unidades.
- `id`, `obra_id`, `escopo_tipo` (enum: `obra_inteira`, `eap`), `escopo_eap_id` (nullable), `criterio` (enum: `fracao_ideal`, `area_privativa`, `igualitario`, `customizado`), `ativo` (bool), `vigente_desde`.
- Default: 1 regra `obra_inteira` + `fracao_ideal`, criada automaticamente ao criar a obra.

#### `regra_rateio_peso_unidade`
Pesos customizados (quando `criterio = customizado`).
- `regra_rateio_id`, `unidade_id`, `peso` (Numeric — normaliza-se na hora do cálculo).

#### `rateio_calculado` *(cache materializado)*
Resultado do cálculo de custo por unidade por EAP.
- `id`, `obra_id`, `unidade_id`, `eap_id` (nullable — null = consolidado da obra), `custo_acumulado`, `calculado_em`.
- Recalcula sob demanda (request de relatório) ou em job assíncrono pós-apropriação.

### 3.8. Vendas

#### `comprador`
- `id`, `tenant_id`, `nome`, `cpf_cnpj`, `contato`, `email`.

#### `venda`
- `id`, `tenant_id`, `unidade_id`, `comprador_id`, `preco_tabela`, `preco_venda_final`, `data_venda`, `status` (enum: `disponivel`, `reservada`, `vendida`, `distratada`), `observacoes`.
- Invariante: uma unidade tem **no máximo uma** venda com status `vendida` ou `reservada` por vez.
- O "status" da unidade é derivado da venda mais recente (ou `disponivel` se não houver).

### 3.9. Análise (views/queries, não tabelas físicas no MVP)

Não são tabelas — são consultas materializadas ou queries on-demand:
- `view_custo_por_unidade(obra_id, unidade_id) → custo_acumulado`
- `view_margem_por_unidade(obra_id, unidade_id) → preco_venda - custo_acumulado` *(visível só ao Proprietário)*
- `view_orcado_vs_realizado(obra_id, eap_id) → (orcado, realizado, delta, %)`
- `view_curva_s(obra_id) → série temporal de desembolso previsto e realizado`

### 3.10. Transversal

#### `audit_log`
- `id`, `tenant_id`, `user_id`, `entidade` (str), `entidade_id` (UUID), `acao` (enum: `create`, `update`, `delete`, `approve`, `cancel`), `payload_antes` (JSONB), `payload_depois` (JSONB), `created_at`.

---

## 4. Diagrama ER (simplificado)

```
Tenant ──< User
  │
  └──< Obra ──< Tipologia ──< Unidade ──< Venda ──> Comprador
        │       └─────────────┘             │
        ├──< EAP (hierárquica)              │
        │     ├──< Orçamento_Item >── Orçamento
        │     ├──< Apropriação_Custo
        │     └──< Cronograma_Etapa
        ├──< RegraRateio ──< PesoUnidade
        ├──< Contrato >── Fornecedor
        │     └──< Medição ──> Apropriação_Custo
        └──< Nota_Fiscal ──< NF_Item ──> Apropriação_Custo
                              └──> Insumo (opcional)

Catálogo (tenant): Insumo, Composição ──< Composição_Insumo
                        │
                        └──> SINAPI_Insumo / SINAPI_Composição (global)
```

---

## 5. Invariantes e regras de negócio críticas

1. **Isolamento de tenant:** toda query no backend passa por um helper que injeta `tenant_id` do request. Testes verificam vazamento.
2. **Soma de frações ideais:** validador na obra emite warning se `SUM(fracao_ideal) ≠ 1.0`. Não bloqueia (construtora pode editar progressivamente).
3. **Orçamento aprovado único:** trigger ou constraint parcial — `UNIQUE(obra_id) WHERE status = 'aprovado'`.
4. **Apropriação não excede NF:** `SUM(apropriacoes.valor) WHERE origem = nf_item.id ≤ nf_item.valor_total` (validado em serviço).
5. **Operacional sem valor financeiro de venda/margem:** middleware de serialização zera/omite campos sensíveis quando `request.user.role == 'operacional'`. Endpoints de venda e margem retornam `403` para Operacional.
6. **NF cancelada:** mantém apropriações? Não — ao cancelar uma NF totalmente apropriada, sistema **exige** que o usuário gere estornos antes (ou os gera automaticamente como ação confirmada).
7. **Snapshot de custo:** `composicao_insumo.custo_unitario_snapshot` e `orcamento_item.custo_unitario` nunca são atualizados retroativamente quando o catálogo muda. Só nascem novos.

---

## 6. Decisões em aberto (não bloqueiam Onda 1)

- **Row Level Security no Postgres** para reforçar isolamento de tenant — avaliar após Onda 1.
- **Particionamento** de `apropriacao_custo` por obra — só relevante em escala (não MVP).
- **Versionamento de SINAPI:** manter histórico completo (todas as versões mensais) ou só últimas N? — começar guardando tudo, otimizar depois.
- **Moeda:** assumindo BRL único. Se algum dia entrar USD (importação), revisitar.
- **Fuso horário:** assumir `America/Sao_Paulo` em toda exibição; persistir em UTC.

---

## 7. Glossário (ubiquitous language)

| Termo | Definição |
|-------|-----------|
| **Obra** | Empreendimento gerido. Tem um terreno, unidades, EAP, orçamentos, lançamentos. |
| **Unidade** | Apartamento individual com identificador único (ex.: Apto 101). |
| **Tipologia** | Modelo de unidade (Tipo A, B, etc) com área e configuração padrão. |
| **Fração ideal** | Percentual legal de cada unidade no terreno e nas áreas comuns. Default para rateio. |
| **EAP** | Estrutura Analítica do Projeto. Árvore de etapas/serviços onde tudo é apropriado. |
| **Insumo** | Material, mão de obra ou equipamento. Unidade básica de custo. |
| **Composição** | Serviço composto por insumos (ex.: "1 m² de alvenaria = X tijolos + Y h pedreiro"). |
| **Orçamento** | Planejamento de custo da obra. Versionado. Tem itens ligados à EAP. |
| **Apropriação** | Ato de dizer "este valor pertence a esta etapa da EAP". Liga lançamento à EAP. |
| **Medição** | Reconhecimento de % executado de um contrato de empreiteiro, gerando custo. |
| **Rateio** | Distribuição do custo de uma etapa entre as unidades, por um critério. |
| **Margem por unidade** | `preco_venda_final - custo_rateado_acumulado` (visível só ao Proprietário). |
| **VGV** | Valor Geral de Vendas — soma dos preços tabela ou vendidos das unidades. |
| **Curva S** | Gráfico cumulativo de desembolso (previsto × realizado) ao longo do tempo. |
| **SINAPI** | Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil (CAIXA/IBGE). Base de referência mensal por UF. |
