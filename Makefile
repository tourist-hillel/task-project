DOCKER_COMPOSE = docker-compose
PYTHON = python

.PHONY: build up down test test-coverage


build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

migrate:
	$(DOCKER_COMPOSE) run backend $(PYTHON) manage.py makemigrations
	$(DOCKER_COMPOSE) run backend $(PYTHON) manage.py migrate

test:
	$(DOCKER_COMPOSE) run backend $(PYTHON) -m pytest

test-coverage:
	$(DOCKER_COMPOSE) run backend coverage run -m pytest
	$(DOCKER_COMPOSE) run backend coverage report
	$(DOCKER_COMPOSE) run backend coverage html --directory=/app/backend/htmlcov
ß
