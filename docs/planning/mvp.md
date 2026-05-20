# Construtor Total — Planejamento do MVP

> Status: **draft v2** — todas as decisões de escopo do MVP travadas. Próximo passo: modelagem de domínio e detalhamento da Onda 1.

---

## 1. Norte (North Star)

> Permitir que uma construtora gerencie uma obra do **orçamento ao fechamento** e calcule **margem real por apartamento** (preço vendido − custo rateado), em conformidade com a realidade fiscal e jurídica brasileira (incorporação imobiliária, fração ideal, NF-e).

Critério de sucesso do MVP: uma construtora real consegue rodar **uma obra inteira** no sistema, do orçamento até o fechamento de custos, e extrair a margem por unidade sem usar planilha paralela.

---

## 2. Princípios de escopo

1. **Custo é o coração.** Qualquer feature que não impacta orçamento, apropriação ou rateio é candidata a ficar fora do MVP.
2. **Realidade brasileira nativa.** Fração ideal, NF-e, SINAPI, incorporação — não é "i18n", é o produto.
3. **Uma obra antes de muitas.** O MVP precisa funcionar perfeitamente para 1 obra de 1 construtora antes de pensar em multi-tenant pesado.
4. **Planilha-killer, não ERP.** Não competimos com SAP/TOTVS. Competimos com o Excel que toda construtora pequena/média usa hoje.

---

## 3. Decisões e perguntas abertas

### 3.1. Decididas (round 1)

| # | Pergunta | Decisão | Implicações |
|---|----------|---------|-------------|
| Q1 | Cliente-alvo | **Construtora pequena** (1-3 obras/ano) | UX simples, poucos perfis de usuário, foco em 1 obra ativa por vez, preço acessível, baixa fricção de onboarding. Sem necessidade de orçamento ultra-detalhado tipo grande incorporadora. |
| Q4 | NF-e | **Upload de XML pelo usuário** | Parser local de XML, sem custo recorrente de provedor SEFAZ, sem certificado digital obrigatório no MVP. Usuário arrasta o XML que o contador/fornecedor já envia por e-mail. |
| Q5 | SINAPI/TCPO | **Entra no MVP como diferencial** | Importer de tabela SINAPI (CSV mensal da CAIXA). Catálogo de composições e insumos pré-populado. Pipeline de atualização mensal. Construtora pequena se beneficia muito por não ter equipe de orçamentista. |
| Q7 | Vendas | **Registro simples** | Preço-tabela, preço de venda final, data, comprador (cadastro mínimo: nome, CPF, contato), status da unidade. Sem proposta/contrato/financiamento/comissão de corretor. |

### 3.2. Decididas (round 2)

| # | Pergunta | Decisão | Implicações |
|---|----------|---------|-------------|
| Q2 | Mono ou multi-tenant? | **Multi-tenant (SaaS)** desde o início. | `tenant_id` em todas as tabelas; isolamento por middleware; auth com escopo por tenant. Sem onboarding manual no MVP — basta self-signup + 1 obra. |
| Q3 | Stack técnica | **Python/FastAPI + PostgreSQL + Next.js** | Backend: FastAPI + SQLAlchemy + Alembic + pytest. Frontend: Next.js (App Router) + TypeScript. Auth: JWT/session via backend. Deploy: container único + Postgres gerenciado. |
| Q6 | Mobile / canteiro | **Fora do MVP.** Web responsivo apenas. | UI **moderna mas com cara de sistema empresarial** — não "app de IA", não gradientes coloridos, não estilo SaaS genérico. Paleta inspirada em construção civil (ver §3.4). |
| Q8 | Contabilidade fiscal | **Fora.** Apenas export de relatórios para o contador. | Sem SPED, sem geração de ISS, sem integração com escritório contábil. |
| Q9 | Patrimônio de afetação | **Fora do MVP**, com gancho no modelo. | Campo `regime_tributario` ou `em_afetacao: bool` na obra desde o schema inicial — sem lógica acoplada. |
| Q10 | Perfis de usuário | **2 perfis: Proprietário e Operacional.** | **Proprietário:** vê tudo, inclusive margens, vendas, custo realizado por unidade, comparativos financeiros. **Operacional:** lança dados (NF, medições, horas, apontamentos de mão de obra), vê quantitativos físicos e prazos — **não vê valores de venda, margem, nem custo consolidado por unidade**. |

### 3.3. Implicações consolidadas

- **Importer SINAPI** é tarefa de primeira ordem (pipeline mensal, CSV CAIXA).
- **Parser XML NF-e** é módulo do MVP — não trivial mas factível (XML padronizado pela SEFAZ).
- **Sem certificado digital** A1/A3 no MVP.
- **Vendas** = CRUD, sem fluxo de aprovação.
- **Multi-tenant** desde o schema (todo cuidado para não vazar dados entre tenants — review de queries, RLS opcional no Postgres a estudar).
- **Visibilidade financeira** é regra de negócio crítica do Operacional: o sistema **nunca pode renderizar valores de venda nem margem** para esse perfil, em nenhuma tela ou relatório.

### 3.4. Diretrizes de design da UI

**Personalidade:** sistema de empresa sério, denso, eficiente. Pensa em "ferramenta de trabalho de engenheiro", não em "landing page de SaaS".

**Evitar:**
- Gradientes coloridos, glass morphism, blur de fundo.
- Paletas roxo/rosa/azul-claro típicas de produtos de IA.
- Ilustrações flat de pessoas felizes, mascotes, emojis na UI.
- Tipografia ultra-grande / hero sections.
- Animações de marketing.

**Buscar:**
- Densidade de informação alta (tabelas, grids, dashboards numéricos legíveis).
- Tipografia técnica (sans-serif neutra: Inter, IBM Plex Sans ou similar).
- Componentes sóbrios, alinhamento rigoroso, grid forte.
- Sensação tátil de ferramenta industrial.

**Paleta inspirada em construção civil** (referência inicial — refinar com designer):
- **Concreto** (cinzas neutros): fundo, superfícies, bordas — `#1f1f1f`, `#3a3a3a`, `#7a7a7a`, `#e5e5e5`.
- **Aço** (azul-acinzentado escuro): cabeçalhos, ações primárias — `#2c3e50` / `#34495e`.
- **Amarelo segurança** / **EPI** (uso pontual, alta saliência): alertas, CTAs críticos, marcações de obra — `#f5a623` / `#ffc107`.
- **Laranja sinalização**: estados de atenção — `#e67e22`.
- **Tijolo/terracota** (acento quente, uso parcimonioso): branding, badges — `#a0522d` / `#c0392b`.
- **Verde** apenas para confirmação/sucesso, tom sóbrio — `#27ae60`.

**Modo escuro:** desejável, mas não bloqueante no MVP.

---

## 4. Módulos propostos para o MVP

> Escopo de referência, sujeito às respostas das perguntas acima.

### 4.1. Cadastros base
- Empreendimento / Obra (terreno, área total, datas previstas).
- Unidades (apartamentos, tipologias, área privativa, área comum, **fração ideal**).
- Fornecedores e prestadores.
- Insumos (materiais, mão de obra, equipamentos).
- Composições de serviço (insumo × quantidade × custo unitário).
- Plano de contas / centros de custo da obra (EAP — Estrutura Analítica do Projeto).

### 4.2. Orçamento (pré-obra)
- Montagem do orçamento por etapa da EAP.
- Quantitativos por serviço.
- Custo previsto total, por etapa, e por m².
- **Versionamento** de orçamentos (orçamento base × revisões).
- Export para PDF/Excel.

### 4.3. Planejamento físico-financeiro
- Cronograma físico (etapas com data início/fim).
- Curva S prevista (desembolso ao longo do tempo).
- Marcos da obra.

### 4.4. Execução (durante a obra)
- Entrada de notas fiscais:
  - Manual.
  - Import de XML NF-e (depende de Q4).
- Apropriação: cada lançamento (NF, medição, folha) vai para uma **etapa da EAP** e um **centro de custo**.
- Medições de contratos de empreiteiros (% executado × valor contratado).
- Comparativo **orçado × realizado** por etapa e acumulado.
- (Stretch) RDO — Relatório Diário de Obra.

### 4.5. Rateio de custos
- Critérios configuráveis por etapa ou tipo de custo:
  - **Fração ideal** (default legal para áreas comuns).
  - **Área privativa.**
  - **Igualitário** entre unidades.
  - **Customizado** (peso por unidade).
- Custo acumulado por unidade — atualiza conforme a obra avança.

### 4.6. Vendas e precificação
- Tabela de vendas: preço-tabela por unidade.
- Status da unidade: disponível, reservada, vendida, distratada.
- Registro da venda: data, valor final, comprador (cadastro mínimo).
- (Definir em Q7 quanto mais.)

### 4.7. Análise (núcleo do produto)
- **Custo realizado por apartamento** (com rateio aplicado).
- **Margem por apartamento:** preço vendido − custo rateado.
- Margem por tipologia.
- VGV (Valor Geral de Vendas) × custo total da obra.
- Comparativo orçado × realizado consolidado.
- Curva S real × prevista.

### 4.8. Infraestrutura
- Autenticação e perfis.
- Audit log de alterações em valores críticos (orçamento, NF, venda).
- Export Excel/PDF dos relatórios principais.
- Backup.

---

## 5. Fora do MVP (explicitamente)

- Folha de pagamento / RH.
- Contabilidade fiscal completa (SPED, DCTF, etc.).
- BIM / integração com projetos 3D.
- CRM imobiliário completo (funil de vendas, corretores, comissões).
- Financiamento ao comprador (associativo, SFH).
- App de cliente final (acompanhamento do comprador).
- Patrimônio de afetação como regime fiscal/contábil completo (modelo de dados deixa o gancho).
- Multi-obra com rateio cruzado entre empreendimentos.

---

## 6. Faseamento sugerido

Sugestão de ondas dentro do "MVP":

**Onda 1 — Esqueleto de custo (validar conceito):**
Cadastros base + Orçamento + Apropriação manual de NF + Rateio + Análise margem por unidade.
→ Já permite rodar uma obra simples e provar o valor central.

**Onda 2 — Realidade operacional:**
Cronograma + Curva S + Medições + Import NF-e + Versionamento de orçamento.

**Onda 3 — Vendas e fechamento:**
Tabela de vendas + Status de unidade + Relatórios de margem + Export.

Cada onda deve estar **utilizável em produção** ao final (não é waterfall disfarçado).

---

## 7. Próximos passos

1. Fechar Q2, Q3, Q6, Q8, Q9, Q10 (round 2 — recomendações já no doc).
2. Modelar o domínio (entidades e relações) — `docs/architecture/domain-model.md`.
3. Detalhar Onda 1 em user stories / tarefas executáveis.
4. Montar esqueleto do repositório com a stack escolhida.
5. Implementar Onda 1.
