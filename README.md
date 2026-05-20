# Construtor Total

Sistema para gestão da construção civil no Brasil, com foco em **gestão de obra e custos** — antes, durante e depois da execução — permitindo precificar cada apartamento com base no custo real e comparar com o preço vendido.

## Status

🚧 Em desenvolvimento — Onda 1 (esqueleto de custo).

- Escopo do MVP: [docs/planning/mvp.md](docs/planning/mvp.md)
- Modelo de domínio: [docs/architecture/domain-model.md](docs/architecture/domain-model.md)
- Plano da Onda 1: [docs/planning/onda-1.md](docs/planning/onda-1.md)

## Stack

- **Backend:** Python 3.12 + FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL 16.
- **Frontend:** Next.js 14 (App Router) + TypeScript.
- **Orquestração local:** Docker Compose.
- **CI:** GitHub Actions.

## Estrutura

```
backend/        # API FastAPI
frontend/       # Next.js 14
docs/
  planning/     # MVP, ondas, decisões
  architecture/ # domain model, ADRs
.github/        # workflows de CI
docker-compose.yml
Makefile
```

## Primeiros passos

```bash
cp .env.example .env
make up                     # sobe db + backend + frontend
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

## Licença

Proprietário. Ver [LICENSE](LICENSE).
