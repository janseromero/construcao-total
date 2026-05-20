# Construtor Total

Sistema para gestão da construção civil no Brasil, com foco em **gestão de obra e custos** — antes, durante e depois da execução — permitindo precificar cada apartamento com base no custo real e comparar com o preço vendido.

## Status

🚧 Em desenvolvimento — **Onda 1 implementada** (esqueleto de custo end-to-end).

- **📘 Tutorial do usuário:** [docs/tutorial/README.md](docs/tutorial/README.md) — guia completo módulo a módulo
- Escopo do MVP: [docs/planning/mvp.md](docs/planning/mvp.md)
- Modelo de domínio: [docs/architecture/domain-model.md](docs/architecture/domain-model.md)
- Plano da Onda 1: [docs/planning/onda-1.md](docs/planning/onda-1.md)

## O que está pronto

**Backend (FastAPI):**
- Auth com signup/login/JWT, perfis Proprietário e Operacional.
- Multi-tenant com isolamento testado.
- CRUD: Obra, Tipologia, Unidade, EAP (hierárquica), Fornecedor, Insumo, Composição.
- Orçamento versionado com aprovação atômica.
- Nota Fiscal + Apropriação à EAP com validação de não-excedente.
- Apontamento de mão de obra (valor oculto para Operacional).
- Lançamento manual de custos (Proprietário).
- Rateio por fração ideal / área privativa / igualitário / customizado, com regras por EAP.
- Análise: custo por unidade, margem por unidade, orçado × realizado, resumo executivo (VGV).
- Vendas + compradores (apenas Proprietário).
- 11 testes verdes (auth, tenant isolation, role guard, rateio, validações).

**Frontend (Next.js 14):**
- Landing, signup, login.
- App shell com sidebar industrial.
- Dashboard, lista de obras, criação de obra.
- Obra: visão geral, unidades, EAP em árvore, orçamento (lista + editor de itens), execução (NF + apropriação modal), análise (3 relatórios), vendas.
- Catálogo: fornecedores, insumos.
- Build de produção limpo (16 rotas).

## Stack

- **Backend:** Python 3.12 + FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL 16.
- **Frontend:** Next.js 14 (App Router) + TypeScript.
- **Orquestração local:** Docker Compose (DB + backend com migrations + frontend).
- **CI:** GitHub Actions (lint + pytest + next build).

## Primeiros passos

```bash
cp .env.example .env
make up                     # sobe db + backend (migra automaticamente) + frontend
# backend  → http://localhost:8000  (docs em /docs)
# frontend → http://localhost:3000
```

Outros comandos: `make help`.

## Princípios

1. Custo é o coração — qualquer feature que não impacta orçamento, apropriação ou rateio é candidata a ficar fora.
2. Realidade brasileira nativa (NF-e, SINAPI, fração ideal, incorporação).
3. Planilha-killer, não ERP — competimos com o Excel da construtora pequena.
4. Multi-tenant por design, isolamento reforçado.
5. UI com cara de ferramenta industrial, sem vibe de "AI app".

## Próximas ondas

- **Onda 2:** cronograma físico-financeiro + curva S, medições de contrato, import XML NF-e, versionamento avançado, importer SINAPI mensal.
- **Onda 3:** polimento de vendas e fechamento, exports refinados, audit log com UI.

## Licença

Proprietário. Ver [LICENSE](LICENSE).
