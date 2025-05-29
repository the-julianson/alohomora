.PHONY: build test test-e2e lint db-shell help clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make build      - Build and start the application using docker-compose"
	@echo "  make test       - Run unit tests (excluding API tests)"
	@echo "  make test-e2e   - Build and run all tests including API tests"
	@echo "  make lint       - Run ruff linter"
	@echo "  make db-shell   - Access the database shell"
	@echo "  make down       - Stop and remove containers"
	@echo "  make clean      - Remove all containers and volumes"
	@echo "  make logs       - View logs"

# Run the full stack
up:
	docker-compose up -d

# Build and start the application
build:
	docker-compose up --build -d

# Run unit tests (excluding API tests)
test:
	docker-compose run --rm web pytest -vs -k "not test_api"

# Run all tests including API tests
test-e2e: build
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

# Remove all containers and volumes
clean:
	docker-compose down -v
	docker container prune -f
	docker volume prune -f

logs:
	docker-compose logs -f