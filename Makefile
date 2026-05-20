.PHONY: help up down logs backend frontend test lint format migrate seed clean

help:
	@echo "Construtor Total - dev commands"
	@echo ""
	@echo "  make up         - sobe docker compose (db + backend + frontend)"
	@echo "  make down       - derruba docker compose"
	@echo "  make logs       - logs do compose"
	@echo "  make backend    - shell no container do backend"
	@echo "  make frontend   - shell no container do frontend"
	@echo "  make test       - roda testes do backend"
	@echo "  make lint       - lint backend + frontend"
	@echo "  make format     - format backend + frontend"
	@echo "  make migrate    - aplica migrations Alembic"
	@echo "  make seed       - popula dados de exemplo (dev)"
	@echo "  make clean      - remove caches e build artifacts"

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

backend:
	docker compose exec backend bash

frontend:
	docker compose exec frontend sh

test:
	docker compose exec backend pytest

lint:
	docker compose exec backend ruff check .
	docker compose exec frontend npm run lint

format:
	docker compose exec backend ruff format .
	docker compose exec frontend npm run format

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python -m app.scripts.seed_dev

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	rm -rf backend/.coverage backend/htmlcov backend/coverage.xml
	rm -rf frontend/.next frontend/out
