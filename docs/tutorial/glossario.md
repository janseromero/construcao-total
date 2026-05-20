# Glossário

Termos técnicos e de negócio usados no Construtor Total. Organizado em ordem alfabética.

---

### Apropriação
Ato de classificar um valor em uma folha da EAP. Diz "este custo pertence a esta etapa". É a operação central do sistema durante a execução da obra. Pode ser fracionada: uma NF de R$ 10.000 pode virar 2 apropriações de R$ 7.000 e R$ 3.000 em etapas diferentes. Ver [cap. 6](06-execucao.md#62-apropriação--o-ato-central-do-sistema).

### Apontamento de mão de obra
Lançamento de horas/dias trabalhados de um funcionário (Pedreiro, Servente, Eletricista...). Gera apropriação automática para a EAP onde aquela mão de obra atuou. O valor monetário fica oculto para o perfil Operacional. Ver [cap. 6](06-execucao.md#63-apontamento-de-mão-de-obra).

### Área comum proporcional
Parte da área comum do empreendimento (escadas, hall, garagem, lazer) atribuída proporcionalmente a uma unidade. Geralmente proporcional à fração ideal, embora possa seguir outra regra dependendo da convenção.

### Área privativa
Área exclusiva de uma unidade (parte interna do apartamento, mais sacada). Excluí áreas comuns. Usada como critério opcional de rateio de custos.

### Bcrypt
Algoritmo de hash usado para guardar senhas no banco. Não é reversível — mesmo o administrador do sistema não consegue ver a senha original.

### CNPJ
Cadastro Nacional da Pessoa Jurídica. Usado como identificador único da construtora (tenant) no Construtor Total.

### Composição
Receita que combina insumos em um serviço. Exemplo: "1 m² de alvenaria = 13 blocos + 0,008 m³ de areia + 0,16 sc de cimento + 0,8 h pedreiro + 1,2 h servente". Permite orçar e lançar de forma agregada. Ver [cap. 4](04-catalogo.md#43-composições).

### Comprador
Cliente final que adquire uma unidade. Cadastro simples (nome, CPF/CNPJ, contato, e-mail). Não há fluxo KYC nem due diligence no MVP.

### Contingência
Reserva financeira no orçamento para imprevistos. Recomenda-se 5–10% do total. Lance como item explícito (ex.: `12.5 Contingência`).

### Contrato
Vínculo formal com um empreiteiro (fornecedor de serviço) para execução de uma parte da obra. Tem valor total e gera medições parciais ao longo da execução. Modelado no schema, mas com UI em ondas futuras.

### CPF
Cadastro de Pessoa Física. Usado em cadastros de comprador ou fornecedor pessoa física (autônomo).

### Cronograma físico-financeiro
Plano de execução com datas previstas por etapa e o quanto se espera desembolsar em cada momento. Origem da Curva S. Entra na Onda 2.

### Curva S
Gráfico cumulativo de desembolso ao longo do tempo. Mostra previsto × realizado. Permite ver se a obra está adiantada, atrasada ou no plano. Entra na Onda 2.

### Custos diretos
Custos diretamente associados à execução física: material, mão de obra, equipamento. Etapas 1–11 da EAP recomendada.

### Custos indiretos
Custos que não são execução física: engenharia, administração, alvarás, taxas, ART, IPTU da obra, seguro, manutenção do canteiro. Etapa 12 da EAP recomendada. **Esquecer estes faz a margem por unidade aparecer falsamente alta.**

### Distrato
Cancelamento de uma venda já registrada. Cliente desiste e contrato é desfeito (com ou sem retenção de sinal). A unidade volta a ficar disponível. No MVP, registre como nova venda com status `distratada`.

### EAP — Estrutura Analítica do Projeto
Árvore hierárquica que decompõe a obra em etapas e sub-etapas. Cada folha é onde se apropriam custos. É a espinha dorsal do sistema. Ver [cap. 3](03-eap.md).

### Em afetação
Flag que indica se uma obra está sob o regime de **Patrimônio de Afetação** (Lei 10.931/2004) — separação patrimonial entre o empreendimento e a incorporadora. Existe no schema mas sem lógica acoplada no MVP.

### Empreitada / Empreiteiro
Contrato em que terceiro executa parte da obra com seus próprios funcionários (estrutura, pintura, instalação elétrica completa). Pagamento por medição ou valor fechado.

### Fornecedor
Pessoa física ou jurídica que entrega material, serviço ou equipamento à obra. Cadastrado no catálogo do tenant. Ver [cap. 4](04-catalogo.md#41-fornecedores).

### Fração ideal
Percentual legal de cada unidade no terreno e nas áreas comuns. Definido na convenção de condomínio. Soma das frações ideais de uma obra = 1,0. Critério padrão de rateio de custos no Construtor Total. Ver [cap. 2](02-obras-e-unidades.md#o-que-é-fração-ideal).

### Insumo
Unidade básica de custo: material, mão de obra ou equipamento. Tem código interno, unidade (kg, h, m³...) e custo unitário de referência. Pode opcionalmente ter código SINAPI. Ver [cap. 4](04-catalogo.md#42-insumos).

### JWT — JSON Web Token
Token de autenticação usado pela API. Quando você faz login, recebe um JWT que é enviado a cada requisição no header `Authorization: Bearer <token>`. Expira em 8 horas (no MVP).

### Lançamento manual
Registro de custo sem NF (alvarás, ISS, ART, IPTU da obra, taxa de contador). Apenas o Proprietário pode lançar. Gera apropriação automática. Ver [cap. 6](06-execucao.md#64-lançamento-manual-de-custo).

### Margem por unidade
Diferença entre preço de venda (final ou tabela) e custo acumulado de uma unidade. É a métrica que dá norte ao produto. Visível apenas para o Proprietário. Ver [cap. 8](08-analise.md#82-margem-por-unidade).

### Medição
Aprovação de % executado de um contrato de empreiteiro, gerando custo. Exemplo: empreiteiro de pintura executou 30% — você aprova medição de 30% × R$ valor_contratado. Modelado, UI em onda futura.

### NCM
Nomenclatura Comum do Mercosul — código de 8 dígitos que classifica produtos no comércio. Aparece nos itens de NF-e. No MVP, é campo opcional.

### NF-e — Nota Fiscal Eletrônica
Documento fiscal digital padrão SEFAZ. Tem chave de acesso de 44 dígitos e XML estruturado. No MVP, lançamento manual. Onda 2 inclui upload de XML.

### Onda
Fase de entrega do roadmap. Cada Onda do MVP entrega valor incremental:
- **Onda 1** — esqueleto de custo (cadastros + orçamento + apropriação manual + rateio + análise).
- **Onda 2** — realidade operacional (cronograma + Curva S + medições + XML NF-e + SINAPI).
- **Onda 3** — vendas e fechamento (relatórios refinados + audit log na UI + exports).

### Operacional (perfil)
Usuário que lança dados de obra (NF, apropriações, apontamentos). Não vê preço de venda, margem, custo consolidado por unidade. Tipicamente engenheiro de campo ou administrativo.

### Orçamento
Plano financeiro da obra. Versionado: rascunho → aprovado → superado. Apenas um aprovado por vez. Ver [cap. 5](05-orcamento.md).

### Patrimônio de afetação
Regime legal (Lei 10.931/2004) de separação patrimonial entre o empreendimento e o restante da incorporadora — protege o cliente em caso de falência. No MVP, apenas a flag `em_afetacao` está no schema.

### Proprietário (perfil)
Usuário com acesso total: orçamento, custo, margem, vendas, configurações. Tipicamente o dono ou sócio da construtora.

### Rateio
Distribuição do custo de uma etapa entre as unidades da obra. Pode ser por fração ideal, área privativa, igualitário ou customizado. Ver [cap. 7](07-rateio.md).

### Rateio calculado (cache)
Tabela de cache que guarda o resultado do cálculo do rateio (custo acumulado por unidade). Refeita on-demand quando você abre o relatório ou clica em "Recalcular rateio".

### Regra de rateio
Definição de como uma sub-árvore da EAP (ou a obra inteira) é rateada. Tem escopo (obra ou EAP específica), critério (fração ideal / área / igualitário / customizado) e, no caso customizado, pesos por unidade.

### Reserva
Status intermediário de uma unidade — cliente sinalizou interesse, mas ainda não fechou. No MVP, sem fluxo automático de expiração — você gerencia manualmente.

### Resumo executivo
Painel sintético com VGV, custo total, margem total, margem %, unidades vendidas. Apenas Proprietário. Aparece na Visão geral da obra.

### Servente
Auxiliar do pedreiro. Insumo de tipo mão de obra. Custo da hora bem menor (≈60–70% do pedreiro), mas a equipe usa em maior quantidade.

### Signup
Criação de conta. Cria automaticamente um tenant + um usuário Proprietário. Ver [cap. 1](01-primeiros-passos.md#11-criar-conta).

### SINAPI
Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil. Mantido pela CAIXA e IBGE. Tabela de referência de preços de insumos e composições, atualizada mensalmente, variando por UF. Será integrada na Onda 2.

### SPED
Sistema Público de Escrituração Digital — obrigações fiscais. **Fora do escopo do MVP.** Use seu sistema contábil para isso.

### Status (de unidade/venda)
Estado atual de uma unidade no fluxo comercial: `disponivel`, `reservada`, `vendida`, `distratada`.

### Status (de obra)
Estado atual da obra: `planejamento`, `em_obra`, `concluida`, `pausada`.

### Status (de NF)
Estado de apropriação: `pendente_apropriacao`, `parcialmente_apropriada`, `totalmente_apropriada`, `cancelada`.

### Status (de orçamento)
`rascunho`, `aprovado`, `superado`. Apenas um aprovado por vez.

### Stack
Conjunto de tecnologias usadas. Construtor Total = Python 3.12 + FastAPI + SQLAlchemy + Postgres (backend) + Next.js 14 + TypeScript (frontend) + Docker Compose (orquestração local).

### Tenant
Cada construtora cadastrada no SaaS é um tenant. Dados ficam isolados — usuários de um tenant nunca enxergam dados de outro. Toda tabela tem `tenant_id`.

### Tipologia
Modelo padrão de unidade (ex.: "Tipo A — 2 dormitórios, 60 m²"). Conveniência para criar várias unidades parecidas rapidamente.

### Unidade
Apartamento físico individual. Tem identificador (101, 102, 201...), área privativa, fração ideal e opcionalmente tipologia.

### UF
Unidade Federativa (estado brasileiro). Obrigatório no cadastro da obra — determina qual tabela SINAPI será usada (a SINAPI varia por estado).

### Venda
Registro de transação comercial: unidade × comprador × preço × data. Apenas Proprietário pode cadastrar. Ver [cap. 9](09-vendas.md).

### Versão de orçamento
Cada vez que você quer reestimar a obra, cria uma nova versão (v1, v2, v3...). Apenas uma aprovada por vez.

### VGV — Valor Geral de Vendas
Soma do preço de venda de todas as unidades. Métrica de receita potencial e efetiva do empreendimento.

### XML NF-e
Arquivo XML padrão SEFAZ que contém todos os dados de uma nota fiscal eletrônica. Onda 2 incluirá upload deste XML para preenchimento automático.

---

[← Voltar ao índice](README.md)
