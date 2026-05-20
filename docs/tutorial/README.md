# Tutorial do Usuário — Construtor Total

Este guia ensina, módulo por módulo, como usar o Construtor Total para gerenciar uma obra do orçamento ao fechamento, calculando margem real por apartamento.

O tutorial foi pensado para **construtoras pequenas** (1–3 obras/ano) e parte do zero: você não precisa de experiência prévia com sistemas de gestão de obra.

---

## Como usar este tutorial

1. **Leia em ordem na primeira vez.** Cada módulo depende do anterior — não dá pra lançar uma nota fiscal antes de cadastrar a obra e o fornecedor.
2. **Siga o exemplo prático.** Em todos os capítulos usamos o mesmo empreendimento fictício, o **Residencial Aurora**, um prédio em São Paulo com 8 apartamentos. Quando terminar o tutorial, você terá uma obra completa lançada no sistema.
3. **Volte aos capítulos como referência.** Cada módulo tem uma seção "Erros comuns" no final — consulte sempre que precisar.

---

## Índice

| # | Módulo | O que você aprende |
|---|--------|--------------------|
| 1 | [Primeiros passos](01-primeiros-passos.md) | Criar conta, entender perfis, navegar pelo sistema |
| 2 | [Obras e unidades](02-obras-e-unidades.md) | Cadastrar a obra, tipologias e apartamentos com fração ideal |
| 3 | [EAP — Estrutura Analítica do Projeto](03-eap.md) | Montar a árvore de etapas/serviços da obra |
| 4 | [Catálogo](04-catalogo.md) | Fornecedores, insumos e composições |
| 5 | [Orçamento](05-orcamento.md) | Criar, editar e aprovar o orçamento versionado |
| 6 | [Execução](06-execucao.md) | Notas fiscais, apropriação, apontamentos e lançamentos manuais |
| 7 | [Rateio](07-rateio.md) | Como o sistema distribui o custo entre os apartamentos |
| 8 | [Análise](08-analise.md) | Custo por unidade, margem e orçado × realizado |
| 9 | [Vendas](09-vendas.md) | Tabela de vendas, status das unidades e VGV |
| 10 | [Fluxo completo de uma obra](10-fluxo-completo.md) | Exemplo end-to-end Residencial Aurora |
| — | [Glossário](glossario.md) | Termos técnicos usados no sistema |

---

## Convenções deste tutorial

- **Negrito** indica nome de tela, botão ou campo.
- `monoespaçado` indica valores literais que você digita ou o sistema mostra.
- Caixas marcadas com 💡 são **dicas práticas**.
- Caixas marcadas com ⚠️ são **avisos importantes** (regras de negócio, validações, casos de uso comum em que se erra).

---

## Antes de começar

Você precisa ter o sistema rodando. Em ambiente de desenvolvimento local:

```bash
make up
```

Acesse:
- Aplicação: `http://localhost:3000` (ou `:3010` em alguns ambientes)
- Documentação da API: `http://localhost:8000/docs` (ou `:8010`)

Em produção, o link é o domínio fornecido pela sua construtora.

---

## Os dois perfis do sistema

O Construtor Total tem **dois perfis de usuário**:

| Perfil | Acesso |
|--------|--------|
| **Proprietário** | Vê e edita tudo. Inclui valores de venda, margem por unidade, custo consolidado, audit log. É o dono ou sócio. |
| **Operacional** | Lança dados de obra (NF, medições, apontamento de mão de obra). **Não vê** preço de venda, margem ou custo consolidado por unidade. É o engenheiro de obra ou o pessoal do administrativo. |

⚠️ A separação não é só visual: o sistema bloqueia no servidor qualquer tentativa do perfil Operacional acessar dados financeiros sensíveis. Pode liberar acesso ao seu pessoal de campo sem medo de vazar margem.

---

Pronto? Comece pelo [capítulo 1 — Primeiros passos](01-primeiros-passos.md).
