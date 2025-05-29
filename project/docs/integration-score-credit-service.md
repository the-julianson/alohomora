## Link to mermaid
https://www.mermaidchart.com/app/projects/11e901d6-6157-42f2-a95a-7f6023f81d55/diagrams/be0b276d-2bec-4611-8748-7365c99f080c/version/v0.1/edit

```
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Queue
    participant CreditScoreService
    participant Database

    Client->>API: POST /borrowers
    API->>Service: create_borrower()
    Service->>Queue: publish_credit_score_request()
    Queue-->>Service: ack
    Service->>Database: save_borrower(credit_score=pending)
    Database-->>Service: borrower_id
    Service-->>API: borrower_id
    API-->>Client: 201 Created

    Note over Queue,CreditScoreService: Async Processing
    Queue->>CreditScoreService: process_credit_score_request()
    CreditScoreService->>CreditScoreService: calculate_credit_score()
    CreditScoreService->>Database: update_credit_score()
    Database-->>CreditScoreService: success
    CreditScoreService-->>Queue: ack
```