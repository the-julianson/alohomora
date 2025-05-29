export function initApp() {
  const app = document.getElementById('app')
  
  // Create navigation
  const nav = document.createElement('nav')
  nav.className = 'bg-white shadow-sm'
  nav.innerHTML = `
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-xl font-bold text-gray-900">Alohomora</h1>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <a href="#" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" data-page="home">Home</a>
            <a href="#" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" data-page="borrower">Create Borrower</a>
            <a href="#" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" data-page="loan">Apply for Loan</a>
          </div>
        </div>
      </div>
    </div>
  `

  // Create main content area
  const main = document.createElement('main')
  main.className = 'max-w-7xl mx-auto py-6 sm:px-6 lg:px-8'
  main.innerHTML = `
    <div class="px-4 py-6 sm:px-0">
      <div id="content"></div>
    </div>
  `

  // Add elements to the app
  app.appendChild(nav)
  app.appendChild(main)

  // Set up navigation
  setupNavigation()
  
  // Show home page by default
  showPage('home')
}

function setupNavigation() {
  const links = document.querySelectorAll('nav a')
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault()
      const page = e.target.dataset.page
      showPage(page)
    })
  })
}

function showPage(page) {
  const content = document.getElementById('content')
  
  switch(page) {
    case 'home':
      content.innerHTML = `
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 mb-4">Welcome to Alohomora</h1>
          <p class="text-xl text-gray-600">Your trusted platform for managing loans and borrowers.</p>
        </div>
      `
      break
    case 'borrower':
      content.innerHTML = `
        <div class="max-w-2xl mx-auto">
          <h1 class="text-2xl font-bold text-gray-900 mb-6">Create New Borrower</h1>
          <form id="borrowerForm" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <input type="text" name="name" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" name="email" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Income</label>
              <input type="number" name="income" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Employment Years</label>
              <input type="number" name="employment_years" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <div class="flex items-center">
              <input type="checkbox" name="has_previous_loans" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
              <label class="ml-2 block text-sm text-gray-900">Has Previous Loans</label>
            </div>
            <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Create Borrower</button>
          </form>
        </div>
      `
      setupBorrowerForm()
      break
    case 'loan':
      content.innerHTML = `
        <div class="max-w-2xl mx-auto">
          <h1 class="text-2xl font-bold text-gray-900 mb-6">Apply for a Loan</h1>
          <form id="loanForm" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Select Borrower</label>
              <select name="borrower_id" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                <option value="">Select a borrower</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Loan Amount</label>
              <input type="number" name="amount" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Term (Months)</label>
              <input type="number" name="term_months" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Purpose</label>
              <input type="text" name="purpose" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
            </div>
            <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Apply for Loan</button>
          </form>
        </div>
      `
      setupLoanForm()
      break
  }
}

function setupBorrowerForm() {
  const form = document.getElementById('borrowerForm')
  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const formData = new FormData(form)
    const data = {
      name: formData.get('name'),
      email: formData.get('email'),
      income: parseInt(formData.get('income')),
      employment_years: parseInt(formData.get('employment_years')),
      has_previous_loans: formData.get('has_previous_loans') === 'on'
    }

    try {
      const response = await fetch('/api/borrowers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        throw new Error('Failed to create borrower')
      }

      const result = await response.json()
      console.log('Borrower created:', result)
      form.reset()
      alert('Borrower created successfully!')
    } catch (error) {
      console.error('Error creating borrower:', error)
      alert('Failed to create borrower. Please try again.')
    }
  })
}

function setupLoanForm() {
  const form = document.getElementById('loanForm')
  const borrowerSelect = form.querySelector('select[name="borrower_id"]')
  let borrowers = [] // Store borrowers in a variable accessible throughout the function

  // Fetch borrowers for the select
  fetch('/api/borrowers')
    .then(response => response.json())
    .then(fetchedBorrowers => {
      borrowers = fetchedBorrowers
      fetchedBorrowers.forEach(borrower => {
        const option = document.createElement('option')
        option.value = borrower.id
        option.textContent = `${borrower.name} (Credit Score: ${borrower.credit_score})`
        borrowerSelect.appendChild(option)
      })
    })
    .catch(error => {
      console.error('Error fetching borrowers:', error)
    })

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const formData = new FormData(form)
    const selectedBorrower = borrowers.find(b => b.id === formData.get('borrower_id'))
    
    if (!selectedBorrower) {
      alert('Please select a borrower')
      return
    }

    const data = {
      borrower: {
        id: selectedBorrower.id,
        name: selectedBorrower.name,
        email: selectedBorrower.email,
        credit_score: selectedBorrower.credit_score,
      },
      amount: parseInt(formData.get('amount')),
      term_months: parseInt(formData.get('term_months')),
      purpose: formData.get('purpose'),
    }

    try {
      const response = await fetch('/api/loans/apply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        throw new Error('Failed to apply for loan')
      }

      const result = await response.json()
      console.log('Loan applied:', result)
      form.reset()
      alert('Loan application submitted successfully!')
    } catch (error) {
      console.error('Error applying for loan:', error)
      alert('Failed to apply for loan. Please try again.')
    }
  })
} 