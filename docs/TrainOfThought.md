# Microloan Platform - Clean Architecture Approach

## Architecture Decision

While the assignment suggests a Layered Architecture, I've chosen to implement Clean Architecture for the following reasons:

1. **Framework Freedom**: Using FastAPI instead of Django gives us the flexibility to implement a more domain-centric architecture without framework constraints.

2. **Domain Independence**: Our core business logic (loan management, investment rules, etc.) should be independent of infrastructure concerns. This makes it:
   - Easier to test
   - Easier to change infrastructure (e.g., switch databases, presentations layer)
   - More maintainable in the long run

3. **Dependency Direction**: In Clean Architecture, dependencies point inward. This means:
   - Trying to follow the dependency inversion where domain layer has no dependencies

4. **Interface Ownership**: Following the principle that "interfaces should be defined where they are used, not where they are implemented", our domain and application layers will define the interfaces they need, and infrastructure will implement them.

## Proposed Core Use Cases

### Loan Management
1. **Create Loan Request**
   - Borrower creates a loan request
   - System validates borrower's credit score
   - System validates loan amount and term
   - System creates and stores the loan request

2. **List Active Loans**
   - Investor views available loans
   - System filters loans by status
   - System allows filtering by amount range
   - System returns loan details

### Investment Management
1. **Create Investment**
   - Investor selects a loan
   - System validates investor's available funds
   - System validates investment amount matches loan
   - System creates investment and updates loan status

2. **Approve/Reject Investment**
   - Borrower reviews investment
   - System validates loan status
   - System updates investment and loan status
   - System handles fund transfers

### Repayment Management
1. **Make Repayment**
   - Borrower makes a payment
   - System validates payment amount
   - System updates investment status
   - System updates loan status
   - System records repayment

## Phase 1 Implementation Plan

1. **Domain Layer**
   - Create domain entities with business rules
   - Define repository interfaces
   - Implement domain events
   - Add validation rules

2. **Repository pattern**
   - Invert the model dependency on orm, have the orm depend ("knows about") on the model 
   - Write tests

3. **Application Layer**
   - Implement use cases
   - Add use case tests

4. **Presentation Layer** (Phase 2)
   - Create API endpoints
   - Implement request/response models
   - Add API documentation
   - Handle error responses

## Testing Strategy

1. **Domain Layer Tests**
   - Unit tests for entities
   - Test business rules
   - Test domain events
   - No infrastructure dependencies

2. **Application Layer Tests**
   - Unit tests for use cases
   - Mock repository interfaces
   - Test use case flows
   - Test error handling

3. **Integration Tests** (Phase 2)
   - Test repository implementations
   - Test API endpoints
   - Test full use case flows
