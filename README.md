## 🚀 Quick Start

Challenge Project 

✅ FastAPI framework with proper endpoints and status codes
✅ Database documentation with Mermaid diagrams
✅ Integration sequence diagram with Mermaid
✅ Layered architecture >> Clean Architecture (missing UoW: Unit of Work still)
✅ Business transformation in service layer ([use cases](BusinessRequirements.md)) 
✅ Data transformation between API and DB
✅ Type hints throughout
✅ ORM usage with SQLAlchemy
✅ Stateless API ready for concurrent users
✅ Health check and version endpoints


### Make Commands
A [Makefile](Makefile) is provided with convenient commands for common tasks like:

```bash
# Run unit tests (excluding API tests)
make test

# Run all tests including API tests
make test-e2e

# Run linter
make lint

# Access database shell
make db-shell

# View logs
make logs

# Clean up containers and volumes
make clean
```

### Build and Run

```bash
# Build the images
docker compose build

# Run the containers
docker compose up -d
```

### Database Migrations

### Testing
For fined grained testing
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


### Other Useful Commands

```bash
# Stop the containers
docker compose stop

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
- **SQLAlchemy ORM** for async database access
- **Pytest** for testing
- **Ruff** for code quality
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

