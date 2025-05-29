# Database Documentation

## Database Schema

## Link to mermaid
https://www.mermaidchart.com/raw/36676355-c490-4b11-949e-f36da5ea2289?theme=light&version=v0.1&format=svg

```mermaid
erDiagram
    BORROWER {
        string id PK "UUID"
        string name
        string email
        int credit_score
    }
    
    INVESTOR {
        string id PK "UUID"
        string name
        string email
        decimal available_funds
    }
    
    LOAN {
        string id PK "UUID"
        string borrower_id FK
        decimal amount
        string purpose
        int term_months
        enum status
        datetime created_at
    }

    INVESTMENT {
        string id PK "UUID"
        string investor_id FK
        string loan_id FK
        decimal amount
        enum status
        datetime created_at
    }

    REPAYMENT {
        string id PK "UUID"
        string investment_id FK
        decimal amount
        date created_at
    }

    BORROWER ||--o{ LOAN : "applies for"
    INVESTOR ||--o{ INVESTMENT : "makes"
    LOAN ||--o| INVESTMENT : "has"
    INVESTMENT ||--o{ REPAYMENT : "receives"
```

## Database Relationships

- A Borrower can have multiple Loans (one-to-many relationship)
- Each Loan belongs to exactly one Borrower
- An Investor can make multiple Investments (one-to-many relationship)
- Each Investment belongs to exactly one Investor
- A Loan can have one Investment (one-to-one relationship)
- An Investment can have multiple Repayments (one-to-many relationship)
- Each Repayment belongs to exactly one Investment

## Integration Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant API as Loan API
    participant Service as Loan Service
    participant DB as Database
    participant External as Credit Score Service

    Client->>API: POST /borrowers
    API->>Service: Create Borrower
    Service->>DB: Save Borrower
    Service->>External: Calculate Credit Score
    External-->>Service: Return Score
    Service->>DB: Update Credit Score
    DB-->>Service: Confirm Update
    Service-->>API: Return Borrower ID
    API-->>Client: Return Response

    Client->>API: POST /loans/apply
    API->>Service: Apply for Loan
    Service->>DB: Get Borrower
    Service->>Service: Check Eligibility
    Service->>DB: Create Loan
    DB-->>Service: Return Loan ID
    Service-->>API: Return Loan ID
    API-->>Client: Return Response

    Note over Client,DB: Future Implementation
    Client->>API: POST /investors
    API->>Service: Create Investor
    Service->>DB: Save Investor
    DB-->>Service: Return Investor ID
    Service-->>API: Return Investor ID
    API-->>Client: Return Response

    Client->>API: POST /investments
    API->>Service: Create Investment
    Service->>DB: Get Investor & Loan
    Service->>Service: Check Available Funds
    Service->>DB: Create Investment
    DB-->>Service: Return Investment ID
    Service-->>API: Return Investment ID
    API-->>Client: Return Response
```

## Notes

1. The database uses SQLAlchemy as the ORM
2. All database operations are performed through the repository pattern
3. The schema is designed to support:
   - Borrower management
   - Investor management
   - Loan applications
   - Investment tracking
   - Repayment tracking
   - Credit score tracking
   - Loan status tracking
4. Currently implemented features:
   - Borrower creation and management
   - Loan application process
5. Future features to be implemented:
   - Investor registration and management
   - Investment creation and tracking
   - Repayment processing
   - Loan status updates 