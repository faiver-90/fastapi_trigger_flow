DC = docker compose
STORAGES_FILE = docker-compose.yaml
EXEC = docker exec - it

### docker, django
# make up                 # Запуск контейнеров (пересборка без кэша + поднятие)
# make down              # Остановка и удаление контейнеров
# make re-create         # Перезапуск контейнеров (без пересборки)
#
# make re-all            # Полный сброс: удалить всё, почистить, пересобрать и запустить
#
# make test              # Запуск Django тестов
# make makemigrations    # Создание новых миграций
# make migrate           # Применение миграций
# make superuser         # Создание суперпользователя
# make shell             # Открытие Django shell в контейнере

.PHONY: up
up:
	docker compose build --no-cache && docker compose up -d

.PHONY: down
down:
	docker-compose down 

.PHONY: test
test:
	${DC} run web python manage.py test

.PHONY: makemigrations
makemigrations:
	${DC} run web python manage.py makemigrations

.PHONY: superuser
superuser:
	${DC} run web python manage.py createsuperuser

.PHONY: shell
shell:
	${DC} run web python manage.py shell

.PHONY: migrate
migrate:
	${DC} run web python manage.py migrate

.PHONY: re-all
re-all:
	docker-compose down -v --remove-orphans
	docker system prune -af --volumes
	docker-compose build --no-cache
	docker-compose up -d --force-recreate

.PHONY: re-create
re-create:
	@docker compose up -d --force-recreate

### Ruff
# make ruff-check        # Проверка без изменений
# make ruff-fix          # Безопасная автоисправка
# make ruff-fix-all      # С полными исправлениями
# make ruff-diff         # Только изменённые файлы
# make ruff-format       # Автоформатирование
# make ruff-format-check # Только проверка форматирования
# make lint              # Всё вместе

# Путь к корню проекта
SRC = .

# Проверка кода (вся директория)
ruff-check:
	ruff check $(SRC)

# Проверка с автоисправлением (безопасные исправления)
ruff-fix:
	ruff check $(SRC) --fix

# Проверка с небезопасными исправлениями (например, удаление импортов)
ruff-fix-all:
	ruff check $(SRC) --fix --unsafe-fixes

# Проверка только изменённых файлов (например, в git)
ruff-diff:
	git diff --name-only --diff-filter=ACMRTUXB HEAD | grep '\.py$$' | xargs ruff check

# Форматирование (если используешь ruff formatter)
ruff-format:
	ruff format $(SRC)

# Проверка форматирования (без изменения)
ruff-format-check:
	ruff format $(SRC) --check

# Удаление .ruff_cache (если используется)
ruff-clean:
	rm -rf .ruff_cache

# Общая команда: проверка и автоисправление
lint: ruff-fix ruff-format
