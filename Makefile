MANAGE := poetry run python manage.py

lint:
	poetry run flake8 task_manager

install:
	poetry install

dev:
	@$(MANAGE) runserver

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

build: install migrate

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
