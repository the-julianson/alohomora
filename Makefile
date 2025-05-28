.PHONY: build test lint db-shell help

# Default target
help:
	@echo "Available commands:"
	@echo "  make build      - Build and start the application using docker-compose"
	@echo "  make test       - Run tests using docker-compose"
	@echo "  make lint       - Run ruff linter"
	@echo "  make db-shell   - Access the database shell"
	@echo "  make down       - Stop and remove containers"

# Build and start the application
build:
	docker-compose up --build -d

# Run tests
test:
	 docker compose exec web pytest -vs

# Run linter
lint:
	docker-compose run --rm web ruff . --check

# Access database shell
db-shell:
	docker-compose exec web-db psql -U postgres -d alohomora

# Stop and remove containers
down:
	docker-compose down 