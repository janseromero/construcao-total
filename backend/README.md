# Construtor Total — Backend

API em FastAPI. Banco PostgreSQL via SQLAlchemy 2 + Alembic.

## Estrutura

```
app/
  core/        # config, segurança
  db/          # base ORM, sessão
  models/      # entidades ORM (ver docs/architecture/domain-model.md)
  routers/     # endpoints
  services/    # regras de negócio (a criar)
  schemas/     # Pydantic (a criar)
alembic/       # migrations
tests/         # pytest
```

## Comandos

A partir da raiz do repo:

```bash
make up                # sobe stack inteira (db + backend + frontend)
make test              # pytest no backend
make lint              # ruff
make migrate           # alembic upgrade head
```

Localmente (sem docker):

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Migrations

```bash
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```
