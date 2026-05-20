# Construtor Total — Onda 1: Esqueleto de Custo

> Status: **planejamento detalhado** — pronto para implementação.

## Objetivo da onda

Provar o valor central do produto: **uma construtora consegue cadastrar uma obra, montar um orçamento, lançar notas fiscais, e ver o custo rateado por apartamento com margem contra o preço vendido** — tudo em uma única ferramenta, sem planilha paralela.

Ao final da Onda 1, o sistema é **utilizável em produção** para uma construtora piloto, com limitações conhecidas (sem cronograma, sem import NF-e XML, sem SINAPI completo, sem medições de contrato — todos esses entram nas Ondas 2 e 3).

## Critérios de aceite da onda

Uma construtora piloto consegue:

1. Criar conta (self-signup), com um tenant e um usuário Proprietário.
2. Cadastrar uma obra com tipologias, unidades e suas frações ideais.
3. Montar a EAP (estrutura analítica) da obra.
4. Cadastrar insumos e composições básicas no catálogo do tenant.
5. Criar um orçamento, lançar itens vinculados à EAP, e aprovar a versão base.
6. Cadastrar fornecedores.
7. Lançar uma nota fiscal manualmente, com itens, e apropriar à EAP.
8. Lançar apontamento de mão de obra (perfil Operacional).
9. Configurar a regra de rateio (default: fração ideal sobre a obra inteira).
10. Visualizar o **custo acumulado por unidade** e a **margem por unidade** (somente Proprietário).
11. Registrar uma venda com preço e comprador.
12. Convidar um usuário Operacional que **não vê** margem, preço de venda nem custo consolidado por unidade.

---

## Stories

Stories estão agrupadas por épico. Cada uma tem: **objetivo**, **critérios de aceite**, **notas técnicas**.

Estimativa relativa: **P** (≤1 dia), **M** (2-4 dias), **G** (≥1 semana).

---

### Épico A — Identidade, autenticação e tenant

#### A1. Self-signup de tenant + primeiro usuário **[M]**
- **Objetivo:** novo cliente cria conta sem intervenção manual.
- **Aceite:**
  - Form `/signup` pede: nome da construtora, CNPJ, nome do usuário, e-mail, senha.
  - Cria `tenant` + `user` com role `proprietario`.
  - Login automático após signup, redireciona para `/onboarding/obra`.
  - Validação: CNPJ formato correto (sem validar dígito no MVP), e-mail único globalmente.
- **Notas:** senha com bcrypt/argon2. JWT em cookie HttpOnly + refresh token.

#### A2. Login e logout **[P]**
- **Aceite:** `/login` valida credenciais, emite sessão; `/logout` invalida.
- **Notas:** rate limit básico (5 tentativas / 15min por IP).

#### A3. Convite de usuário Operacional **[M]**
- **Objetivo:** Proprietário convida pessoa do operacional por e-mail.
- **Aceite:**
  - Tela `/configuracoes/usuarios` com lista e botão "Convidar".
  - Convite gera token de uso único válido 7 dias; e-mail enviado (no MVP: log no console + endpoint de inspeção em dev).
  - Convidado define senha ao aceitar.
- **Notas:** stub de envio de e-mail no MVP (provider real fica para depois).

#### A4. Middleware de tenant e role **[P]**
- **Objetivo:** garantir isolamento em todas as rotas.
- **Aceite:**
  - Helper `get_current_user()` extrai user + tenant + role da sessão.
  - Helper `require_role('proprietario')` para rotas restritas.
  - Toda query passa por `tenant_scoped(session, tenant_id)` — utilitário central.
  - Testes: usuário do tenant A não acessa nenhuma entidade do tenant B (suite de "tenant isolation").

---

### Épico B — Cadastro de obra e estrutura física

#### B1. CRUD de obra **[M]**
- **Aceite:**
  - Campos: nome, endereço, UF, datas previstas, área total, área terreno, status, `em_afetacao` (bool default false).
  - Lista de obras do tenant; só uma "obra ativa" por vez na UI (seletor no topo).
  - Validação: UF obrigatória (define SINAPI futura).

#### B2. CRUD de tipologia **[P]**
- **Aceite:** lista de tipologias por obra; campos: nome, área privativa, área comum proporcional, descrição.

#### B3. CRUD de unidade **[M]**
- **Aceite:**
  - Campos: identificador, andar, bloco (nullable), tipologia, fração ideal, área privativa (snapshot da tipologia, editável).
  - Tela de "alocação em massa": criar N unidades a partir de uma tipologia em uma faixa de andares.
  - Indicador visível da **soma de frações ideais** da obra; warning se ≠ 1.0.

#### B4. CRUD de EAP (árvore) **[M]**
- **Aceite:**
  - Tela em árvore (drag-drop opcional, mas reordenação por botões aceitável).
  - Código sugerido automaticamente (1, 1.1, 1.1.1...).
  - Template inicial: oferece importar uma EAP padrão pré-definida ao criar a obra ("Aceitar template padrão" ou "Começar vazio").
- **Notas:** template padrão = JSON versionado no código com ~30 etapas típicas (Serviços Preliminares, Fundação, Estrutura, Alvenaria, Instalações, Acabamentos, Pintura, Limpeza Final).

---

### Épico C — Catálogo

#### C1. CRUD de fornecedor **[P]**
- **Aceite:** campos do modelo; busca por nome/CNPJ.

#### C2. CRUD de insumo **[M]**
- **Aceite:**
  - Campos do modelo; tipo (material/mão de obra/equipamento).
  - Vínculo opcional a SINAPI: campo "código SINAPI" (no MVP, apenas guarda a string — sem importer ainda).
- **Notas:** importer SINAPI completo entra em onda separada. Onda 1 deixa o gancho.

#### C3. CRUD de composição **[M]**
- **Aceite:**
  - Cabeçalho + tabela de insumos com coeficientes.
  - Custo unitário calculado mostrado em tempo real.
  - Snapshot de custo unitário do insumo gravado em cada linha de `composicao_insumo`.

---

### Épico D — Orçamento

#### D1. Criar orçamento versionado **[M]**
- **Aceite:**
  - Botão "Novo orçamento" cria versão `N+1` em status `rascunho`.
  - Aprovar: muda anterior aprovado para `superado` (transação atômica).
  - Lista de orçamentos da obra com status.

#### D2. Itens de orçamento **[G]**
- **Aceite:**
  - Tela de edição com a árvore da EAP à esquerda, itens à direita.
  - Adicionar item: escolhe folha da EAP + composição (ou item livre) + quantidade.
  - Custo unitário e total calculados; totais por nó da EAP rolam para cima.
  - Snapshot de descrição, unidade e custo unitário no item.

#### D3. Visão consolidada do orçamento **[M]**
- **Aceite:**
  - Tabela com totais por etapa raiz da EAP, % do total, custo por m².
  - Export para Excel (.xlsx) e PDF.

---

### Épico E — Execução

#### E1. Lançamento manual de NF **[M]**
- **Aceite:**
  - Form: fornecedor, número, série, data emissão, valor total, itens (descrição, qtd, unidade, valor unitário, valor total).
  - Salva como `nota_fiscal` + N `nota_fiscal_item`. Status inicial `pendente_apropriacao`.

#### E2. Apropriação de NF à EAP **[G]**
- **Aceite:**
  - Tela de detalhe da NF mostra cada item e botão "Apropriar".
  - Modal permite dividir o valor em múltiplas apropriações (cada uma com EAP folha + valor).
  - Sistema impede `SUM(apropriações) > valor_item`.
  - Status da NF atualiza automaticamente: `pendente` → `parcialmente_apropriada` → `totalmente_apropriada`.
- **Notas:** este é o ponto mais sensível do MVP. Investir em UX. Atalhos: "apropriar 100% nesta EAP".

#### E3. Apontamento de mão de obra (Operacional) **[M]**
- **Aceite:**
  - Tela `/apontamento` acessível ao perfil Operacional.
  - Form: data, EAP, insumo (mão de obra), horas, observação.
  - Custo é calculado mas **não exibido** para Operacional — só o Proprietário vê.
  - Gera `apropriacao_custo` automática.

#### E4. Lançamento manual de custo (avulso) **[P]**
- **Aceite:**
  - Para Proprietário lançar custos sem NF (taxas, emolumentos, etc).
  - Form: data, EAP, valor, descrição, fornecedor (opcional).

---

### Épico F — Rateio e análise

#### F1. Regra de rateio padrão **[P]**
- **Aceite:**
  - Ao criar obra, cria automaticamente `regra_rateio` com `criterio = fracao_ideal`, escopo `obra_inteira`.
  - Tela `/obra/{id}/rateio` mostra a regra ativa e permite editar critério.

#### F2. Regras de rateio por EAP **[M]**
- **Aceite:**
  - Permite adicionar regra específica para uma sub-árvore da EAP (sobrescreve a regra geral).
  - Critérios disponíveis: fração ideal, área privativa, igualitário, customizado.
  - Para customizado: tela para definir peso por unidade.

#### F3. Cálculo de custo por unidade **[G]**
- **Aceite:**
  - Serviço `calcular_rateio(obra_id)` que percorre todas as `apropriacao_custo`, aplica a regra vigente para cada EAP, distribui em `rateio_calculado`.
  - Trigger: ao salvar nova apropriação, marca obra como "rateio desatualizado"; recálculo manual via botão "Recalcular" + job assíncrono.
  - Performance: para 100 unidades × 5.000 apropriações deve rodar em <5s.

#### F4. Relatório de custo por unidade **[M]**
- **Aceite:**
  - Tela `/obra/{id}/analise/custo-por-unidade`.
  - Tabela: unidade, área, fração ideal, custo acumulado, custo por m².
  - Drilldown: clicar na unidade abre detalhamento por EAP.
  - Export Excel/PDF.

#### F5. Relatório de margem por unidade **[M]** *(somente Proprietário)*
- **Aceite:**
  - Tela `/obra/{id}/analise/margem`.
  - Tabela: unidade, custo acumulado, preço de venda, margem (R$ e %).
  - Resumo: VGV total, custo total, margem total da obra.
  - Endpoint backend retorna **403** para Operacional.

#### F6. Relatório orçado × realizado **[M]**
- **Aceite:**
  - Tela `/obra/{id}/analise/orcado-vs-realizado`.
  - Tabela por etapa da EAP: orçado (do orçamento aprovado), realizado (soma de apropriações), delta, %.
  - Indicador visual de extrapolação (>100% realizado).
  - Visível ao Operacional **sem coluna de margem ou venda**.

---

### Épico G — Vendas

#### G1. CRUD de comprador **[P]**
- **Aceite:** campos do modelo.

#### G2. Registro de venda **[M]**
- **Aceite:**
  - Tela `/obra/{id}/vendas`.
  - Lista de unidades com status (disponível, reservada, vendida, distratada).
  - Botão "Vender" abre form: comprador (existente ou novo), preço tabela, preço final, data, observações.
  - Botão "Distratar" muda status, mantém histórico.
  - **403 para Operacional** em todos os endpoints.

#### G3. Tabela de vendas / VGV **[P]**
- **Aceite:**
  - Visão consolidada: total de unidades, vendidas, disponíveis, VGV vendido, VGV potencial.

---

### Épico H — Transversais

#### H1. Audit log **[M]**
- **Aceite:**
  - Eventos registrados: create/update/delete de obra, unidade, orçamento, NF, apropriação, venda; aprovação de orçamento; mudança de role.
  - Tela `/configuracoes/auditoria` (somente Proprietário) com filtros por entidade, usuário, data.

#### H2. Configurações do tenant **[P]**
- **Aceite:** edição de dados da construtora (nome, CNPJ, etc).

#### H3. UI base + navegação **[M]**
- **Aceite:**
  - Layout com sidebar (Obras, Catálogo, Configurações), header com seletor de obra ativa, breadcrumbs.
  - Aderente às diretrizes de design (`docs/planning/mvp.md §3.4`): paleta concreto/aço/amarelo segurança, densidade alta, sem vibe de "AI app".
  - Responsivo até 1024px (web responsivo, não mobile-first).

#### H4. Onboarding **[P]**
- **Aceite:**
  - Após signup, wizard mínimo: criar primeira obra → primeira tipologia → primeiras unidades → confirmação.
  - Pular tudo é permitido (acesso direto ao dashboard vazio).

---

## Sequência de implementação sugerida

Ordem que entrega valor incremental e minimiza retrabalho:

1. **Fundação técnica:** A4 (middleware), banco rodando, migrations iniciais, layout base (H3).
2. **Identidade:** A1, A2, A3.
3. **Obra física:** B1 → B2 → B3 → B4.
4. **Catálogo:** C1 → C2 → C3.
5. **Orçamento:** D1 → D2 → D3.
6. **Execução básica:** E1 → E2 → E4 → E3.
7. **Rateio:** F1 → F3 → F4 → F2 → F6 → F5.
8. **Vendas e fechamento:** G1 → G2 → G3.
9. **Polimento:** H1, H2, H4, ajustes de UX.

## Definition of Done por story

- Código com testes (unitários onde faz sentido, integração para endpoints).
- Migrations Alembic geradas e revisadas.
- Lint passando (`ruff` backend, `eslint` frontend).
- CI verde.
- Documentação curta no `docs/` quando a feature introduzir conceito novo.
- Validação manual em ambiente local com seed mínimo.

## Métricas para encerrar a Onda 1

- Construtora piloto roda 1 obra completa no sistema.
- Bug rate < 1 crítico/semana após 2 semanas em produção.
- Tempo médio para lançar uma NF + apropriar: < 90 segundos.
- Cálculo de rateio para obra com 50 unidades + 1.000 apropriações: < 3s.
