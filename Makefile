DC = docker compose
STORAGES_FILE = docker-compose.yaml
EXEC = docker exec - it

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
