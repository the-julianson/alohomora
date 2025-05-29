
###  CRUD Operations
-    Status: Applied to Some Extent
-    Current: Basic CRUD for borrowers and loans
-    Missing: Batch operations
-    Action: Add batch endpoints for borrowers and loans
###  Dependency Locking
-    Status: Not Applied
-    Current: No dependency lock file
-    Action: Add poetry.lock or requirements.txt
###  Logging
-    Status: Applied
-    Current: Comprehensive logging throughout codebase
-    Action: None needed
###  Problem Details (RFC 9457)
-    Status: Not Applied
-    Current: Basic error responses
-    Action: Implement RFC 9457 error format
###  Correlation ID Middleware
-    Status: Not Applied
-    Current: No correlation tracking
-    Action: Add middleware with UUID generation
###  CSV Processing
-    Status: Not Applied
-    Current: No CSV endpoints
-    Action: Add CSV upload and processing endpoint
###  Pagination
-    Status: Not Applied
-    Current: No pagination
-    Action: Implement both offset and cursor-based pagination
###  Testing with Pytest
-    Status: Applied
-    Current: Unit tests, integration tests, database tests
-    Action: Add more test coverage
###  Dependency Injection
-    Status: Applied
-    Current: Using FastAPI's dependency injection
-    Action: None needed
###  Repository Pattern with Generics
-    Status: Applied to Some Extent
-    Current: Basic repository pattern
-    Action: Add generic repository base class
###  Inversion of Control
-    Status: Applied
-    Current: Using dependency injection and interfaces
-    Action: None needed
###  Domain-Driven Design
-    Status: Applied to Some Extent
-    Current: Basic domain entities
-    Action: Strengthen domain model separation
###  Quality Gates
-    Status: Applied to Some Extent
-    Current: Ruff for linting
-    Action: Add Pylint and Mypy
###  Docker Container
-    Status: Fully Embraced
-    Current: Multi-stage Dockerfile, Docker Compose
-    Action: None needed
###  Hosted DB
-    Status: Not Applied
-    Current: Api in Heroku, DB in Neon, not running though.
-    Action: Deploy Frontend in Fastify and have the fullstack running.
###  Filter Records
-    Status: Not Applied
-    Current: Basic retrieval
-    Action: Add filtering capabilities
###  Rate Limiting
-    Status: Not Applied
-    Current: No rate limiting
-    Action: Add rate limiting middleware
###  Caching
-    Status: Not Applied
-    Current: No caching
-    Action: Add caching for expensive operations
###  Authentication/Authorization
-    Status: Not Applied
-    Current: No security
-    Action: Add JWT or OAuth2
###  RESTFUL API (Richardson Levels)
-    Status: Applied to Some Extent
-    Current: Basic REST implementation
-    Action: Add HATEOAS
###  Performance Metrics
-    Status: Not Applied
-    Current: No metrics
-    Action: Add performance testing
###  API Versioning
-    Status: Applied
-    Current: Using /v1 prefix
-    Action: None needed
###  Simple UI
-    Status: Applied using Vanilla JS and Vite as bundler
-    Current: Basic UI
-    Action: Add more use cases UI
###  GraphQL
-    Status: Not Applied
-    Current: No GraphQL
-    Action: Add GraphQL endpoint
###  CQRS Pattern
-    Status: Not Applied
-    Current: No CQRS
-    Action: Implement CQRS
###  Database Migrations
-    Status: Not Applied
-    Current: No migrations
-    Action: Add Alembic