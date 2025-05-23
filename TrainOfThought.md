# Microloan Platform - Train of Thought

## Core Business Logic

### 1. Loan Request Flow
- Borrower wants money
- They input:
  - Amount needed
  - What they need it for (purpose)
  - How long they need to pay back (timeframe)
- System creates a Loan with status "Active"
- This means the loan is available for investors to see

### 2. Investment Flow
- Investor wants to make money
- They can:
  - See all active loans
  - Filter loans by amount (min/max)
  - Choose a loan to invest in
- When they invest:
  - System creates an Investment
  - Status is "Pending-Borrower-Approval"
  - Borrower needs to say yes or no

### 3. Borrower Approval Flow
- Borrower sees new investment
- They can:
  - Accept the investment
  - Reject it (maybe they found better terms)
- If accepted:
  - Investment status changes to "Active"
  - Money is ready for borrower

### 4. Repayment Flow
- Borrower needs to pay back
- They can make partial payments
- Each payment:
  - Reduces the total amount owed
  - Updates the investment balance
  - Keeps track of payment history

## Technical Approach

### Phase 1: Core Logic (Current Focus)
- Create domain models
- Write business logic
- Add tests
- No API endpoints yet
- Use dummy data for testing

### Phase 2: API & Frontend
- Add REST endpoints
- Create frontend

### Phase 3: Extra Features
- Email notifications
- Payment processing
- Reports and analytics
- Admin dashboard
- Add real user management
- Add real authentication

## Questions to Think About
1. What happens if borrower rejects investment?
2. Can multiple investors invest in same loan?
3. How to handle partial investments?
4. What if borrower can't pay back?
5. How to calculate interest?

## Next Steps
1. Create core models
2. Add business logic
3. Write tests
4. Create dummy data
5. Test core flows 