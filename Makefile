
include local.env
export

lock-deps:
	uv pip compile requirements.in -o requirements.txt

sync-deps:
	uv pip sync requirements.txt

image-build:
	docker-compose build

up-service:
	docker-compose up -d

up-db:
	docker-compose up -d db

generate-migration:
ifeq ($(origin message), undefined)
	echo Usage: make generate-migration message="<new-migration-description>"
	exit 1
endif
	alembic revision  --autogenerate -m $(message)
	git add src/migrations/versions/*.py

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1