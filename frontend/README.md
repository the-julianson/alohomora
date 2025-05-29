# Loan Management System Frontend

A simple frontend for the loan management system built with Vanilla JavaScript and Tailwind CSS.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Features

- Create new borrowers
- Apply for loans
- View loan status
- Responsive design with Tailwind CSS

## API Endpoints

The frontend expects the following API endpoints to be available:

- `POST /borrowers` - Create a new borrower
- `GET /borrowers` - Get all borrowers
- `POST /loans/apply` - Apply for a loan 