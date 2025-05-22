# FastAPI TDD Docker Project
badge.svg?branch=main)

A template for Test-Driven Development (TDD) with FastAPI, Docker, and modern Python tooling.

## 🚀 Quick Start

### Build and Run

```bash
# Build the images
docker compose build

# Run the containers
docker compose up -d
```

### Database Migrations

```bash
# Apply migrations
docker compose exec web aerich upgrade

# (Optional) Apply latest changes to the database without migrations
# docker compose exec web python app/db.py
```

### Testing

```bash
# Run all tests
docker compose exec web python -m pytest

# Disable warnings
docker compose exec web python -m pytest -p no:warnings

# Run only the last failed tests
docker compose exec web python -m pytest --lf

# Run tests matching a string expression
docker compose exec web python -m pytest -k "summary and not test_read_summary"

# Stop after the first failure
docker compose exec web python -m pytest -x

# Enter PDB after first failure
docker compose exec web python -m pytest -x --pdb

# Stop after two failures
docker compose exec web python -m pytest --maxfail=2

# Show local variables in tracebacks
docker compose exec web python -m pytest -l

# List the 2 slowest tests
docker compose exec web python -m pytest --durations=2

# Run tests with coverage
docker compose exec web python -m pytest --cov="."
```

### Linting & Formatting

```bash
# Lint with flake8
docker compose exec web flake8 .

# Check code formatting with Black and isort
docker compose exec web black . --check
docker compose exec web isort . --check-only

# Auto-format code with Black and isort
docker compose exec web black .
docker compose exec web isort .
```

### Other Useful Commands

```bash
# Stop the containers
docker compose stop

# Bring down the containers
docker compose down

# Force a build (no cache)
docker compose build --no-cache

# Remove all images
docker rmi $(docker images -q)
```

### Postgres

```bash
# Access the database via psql
docker compose exec web-db psql -U postgres

# Then, inside psql:
# \c web_dev
# select * from textsummary;
```

---

## 🛠️ Tooling

- **FastAPI** for the web API
- **Tortoise ORM** for async database access
- **Aerich** for migrations
- **Pytest** for testing
- **Black, isort, flake8** for code quality
- **Docker Compose** for orchestration

---

## 🤝 Contributing

1. Fork the repo and clone it.
2. Create a new branch: `git checkout -b my-feature`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to your fork: `git push origin my-feature`
5. Open a Pull Request!


---

Happy coding!

