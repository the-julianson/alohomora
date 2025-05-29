Challenge Project 

This started as a challenger project, with an open approach in terms of what to work with (The business side) and a strict focus on system design. My approach was to create and initial ([train of thought document](docs/TrainOfThought.md\)) which allowed me to start organizing my ideas and set the direction I wanted to go >> Start small, write the business logic first and encapsulate that behaviour without thinking too much on external systems. After some iteration I came with a more detailed plan written in the([business requirements](docs/BusinessRequirements.md)). One thing that I had in mind, was to take the opportunity of learning Clean Architecture in Python by just building something. 

What is still missing: Leveraging the ability of FastAPI together with Starlette and Uvicorn to handle concurrency through the async/await process. I will start working with that together with adding the extra use-cases mentioned in the documentation but not yet applied. 


## Initial Requirements
- #### FastAPI framework with proper endpoints and status codes
- #### Database documentation with Mermaid diagrams ([DB diagram](docs/database.md/#database-schema))
- #### Potential integration sequence diagram using Mermaid ([Integration Diagramn](docs/credit_score_integration.md)) 
- #### Layered architecture >> Clean Architecture (missing UoW: Unit of Work still)
- #### Business transformation in service layer ([use cases](docs/BusinessRequirements.md)) 
- #### Data transformation between API and DB 
- #### Type hints throughout
- #### ORM usage with SQLAlchemy
- #### Stateless API ready for concurrent users
- #### Health check and version endpoints

### How to start playing around

Clone the repo and run `make build` (See more make commands below) to have your application running, internally they are connected and networked through Docker-Compose.
The presentation Layer UI is running in http://localhost:5137
API is running in port 8004, you can see a list of available endpoints at http://localhost:8004/docs 


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
(Not implemented yet)

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

## Tooling used

- **FastAPI** for the web API
- **SQLAlchemy ORM** for async database access
- **Pytest** for testing
- **Ruff** for code quality\
- **JS and TS, HTML and CSS with Tailwind** for the UI presentation layer
- **Vite** For bundling and handling routing between Frontend and the API
- **Docker Compose** for orchestration

---

## This started as a challenger, but feel free to contributing or just using it for learning purposes

1. Fork the repo and clone it.
2. Create a new branch: `git checkout -b my-feature`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to your fork: `git push origin my-feature`
5. Open a Pull Request!

---

Connect with me if you are interested, same as me, in writting clean architectures using python and javascript!
Happy coding!

