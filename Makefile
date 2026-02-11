"""Makefile for common development tasks."""
.PHONY: help install run test lint format clean docker-up docker-down db-init

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Clean up temporary files"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make db-init       - Initialize database"

install:
	pip install -r backend/requirements.txt

run:
	cd backend && uvicorn app.main:app --reload

test:
	pytest backend/tests -v

lint:
	black backend/app --check
	isort backend/app --check
	flake8 backend/app

format:
	black backend/app
	isort backend/app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist build *.egg-info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

db-init:
	psql -U postgres postgres < init-db.sql

migrate:
	cd backend && alembic upgrade head

.DEFAULT_GOAL := help
