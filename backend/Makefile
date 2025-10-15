up:
	@docker compose up -d --build app

down:
	@docker compose down

logs:
	@docker compose logs -f app

seed:
	@docker compose exec app python scripts/load_seed.py

migrate:
	@docker compose exec app alembic upgrade head

fmt:
	@docker compose exec app black src
	@docker compose exec app ruff check --fix src

typecheck:
	@docker compose exec app mypy src

build:
	@docker compose build app

rebuild:
	@docker compose down || true
	@docker compose build --no-cache app
	@docker compose up -d app
