# ==============================================================================
# ⚙️ КОНФИГУРАЦИЯ
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

up: ## 🚀 Запустить локальное окружение
	$(COMPOSE) up

down: ## 🛑 Остановить окружение
	$(COMPOSE) down

build: ## 🔨 Собрать dev Docker образ
	$(COMPOSE) build

rebuild: ## ♻️ Пересобрать и запустить
	$(COMPOSE) up --build --force-recreate

logs: ## 📋 Смотреть логи контейнера
	$(COMPOSE) logs -f $(SERVICE)

status: ## 📊 Статус контейнеров
	$(COMPOSE) ps

exec: ## 🐚 Открыть shell внутри контейнера
	$(EXEC_IT) /bin/sh


# 🎨 ЛИНТЕР И ФОРМАТИРОВАНИЕ

format: ## 🎨 Проверить форматирование (ruff format --check)
	$(EXEC) ruff format --check .

lint: ## 🔍 Проверить линтером (ruff check)
	$(EXEC) ruff check .

format-fix: ## ✏️ Исправить форматирование (ruff format)
	$(EXEC) ruff format .

lint-fix: ## ✏️ Исправить ошибки линтера (ruff check --fix)
	$(EXEC) ruff check --fix .


# ✅ ТЕСТЫ

test: ## ✅ Запустить все тесты
	$(EXEC) pytest .

test-cov: ## 📈 Запустить тесты с покрытием
	$(EXEC) pytest --cov=. --cov-report=term-missing .


# 🗄️ БАЗА ДАННЫХ

migrate: ## 🔄 Применить миграции БД
	$(EXEC) python manage.py migrate

makemigrations: ## 📝 Создать новые миграции
	$(EXEC) python manage.py makemigrations

db-check: ## 🕵️ Проверить наличие непримененных миграций
	$(EXEC) python manage.py migrate --check

collectstatic: ## 📸 Собрать статические файлы
	$(EXEC) python manage.py collectstatic --noinput

shell: ## 🐚 Открыть Django shell
	$(EXEC_IT) python manage.py shell
