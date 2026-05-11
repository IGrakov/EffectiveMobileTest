# ==============================================================================
# ⚙️ CONFIGURATION
# ==============================================================================

COMPOSE ?= docker compose --env-file .env.dev -f compose.yml -f compose.dev.yml
SERVICE ?= web
EXEC    ?= $(COMPOSE) exec -T $(SERVICE)
EXEC_IT ?= $(COMPOSE) exec -it $(SERVICE)

.DEFAULT_GOAL := help

.PHONY: help up down build rebuild logs status exec \
        test test-cov lint format format-fix lint-fix \
        migrate makemigrations db-check collectstatic shell


# 🐳 DOCKER

up: ## 🚀 Launch local environment
	$(COMPOSE) up

down: ## 🛑 Shut down local environment
	$(COMPOSE) down

build: ## 🔨 Build dev Docker image
	$(COMPOSE) build

rebuild: ## ♻️ Re-build and launch
	$(COMPOSE) up --build --force-recreate

logs: ## 📋 See container logs
	$(COMPOSE) logs -f $(SERVICE)

status: ## 📊 Container status
	$(COMPOSE) ps

exec: ## 🐚 Open shell inside container
	$(EXEC_IT) /bin/sh


# 🎨 LINTER AND FORMATTING

format: ## 🎨 Check formatting (ruff format --check)
	$(EXEC) ruff format --check .

lint: ## 🔍 Check by linter (ruff check)
	$(EXEC) ruff check .

format-fix: ## ✏️ Apply formatting (ruff format)
	$(EXEC) ruff format .

lint-fix: ## ✏️ Apply linting (ruff check --fix)
	$(EXEC) ruff check --fix .


# ✅ TESTS

test: ## ✅ Launch all tests
	$(EXEC) pytest .

test-cov: ## 📈 Launch tests with coverage
	$(EXEC) pytest --cov=. --cov-report=term-missing .


# 🗄️ DATABASE

migrate: ## 🔄 Apply migrations in DB
	$(EXEC) python manage.py migrate

makemigrations: ## 📝 Create new migrations
	$(EXEC) python manage.py makemigrations

db-check: ## 🕵️ Check is there any unapplied migrations
	$(EXEC) python manage.py migrate --check

collectstatic: ## 📸 Collect static files
	$(EXEC) python manage.py collectstatic --noinput

shell: ## 🐚 Opem Django shell
	$(EXEC_IT) python manage.py shell
