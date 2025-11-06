.PHONY: dev prod build up down test lint api ui

dev:
	docker compose --profile dev up --build

prod:
	docker compose --profile prod up --build -d

build:
	docker build -t scs-mediator-sdk:latest .

up:
	docker compose up --build

down:
	docker compose down

test:
	pip install -e .[dev] && pytest -q

lint:
	pip install ruff && ruff src

api:
	uvicorn scs_mediator_sdk.api.server:app --reload

ui:
	SCS_API_URL=http://localhost:8000 streamlit run src/scs_mediator_sdk/ui/streamlit_app.py
