SHELL := /bin/sh

PROJECT_NAME = review-it

# Function to determine Docker Compose command
define docker_compose_cmd
	$(if $(shell command -v docker-compose 2> /dev/null),docker-compose,$(if $(shell command -v docker compose 2> /dev/null),docker compose,))
endef


prepare-env:
	cp env-sample .env

up:
	$(call docker_compose_cmd) up

upd:
	$(call docker_compose_cmd) up -d

down:
	$(call docker_compose_cmd) down

stop:
	$(call docker_compose_cmd) stop

build:
	$(call docker_compose_cmd) build

rebuild:
	$(call docker_compose_cmd) build --no-cache

makemigrations:
	$(call docker_compose_cmd) exec review-it python manage.py makemigrations

migrate:
	$(call docker_compose_cmd) exec review-it python manage.py migrate

exec:
	$(call docker_compose_cmd) exec review-it /bin/bash

db-exec:
	$(call docker_compose_cmd) exec mariadb /bin/bash

generate-docs:
	$(call docker_compose_cmd) exec review-it python manage.py generate_swagger > swagger.yaml
