
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