# Restful-Booker API Tests

This project contains automated API tests for the [Restful-Booker API](https://restful-booker.herokuapp.com/), a sample hotel booking REST API for testing and practicing API automation.

Here is the detailed README file of test checklist [restful-booker-api-test-checklist.md](restful-booker-api-test-checklist.md)

## About Restful-Booker API

Restful-Booker is a web service that provides a RESTful API for hotel booking operations. It supports CRUD operations for managing bookings and includes authentication capabilities.

**Base URL:** `https://restful-booker.herokuapp.com`

## API Endpoints Under Test

All endpoints of the Restful-Booker API are covered in this test suite:

### Authentication
- **POST** `/auth` - Create authentication token

### Booking Operations
- **GET** `/booking` - Get all booking IDs
- **GET** `/booking?firstname=value&lastname=value` - Get filtered bookings
- **GET** `/booking/:id` - Get specific booking details
- **POST** `/booking` - Create a new booking
- **PUT** `/booking/:id` - Update an existing booking (requires authentication)
- **PATCH** `/booking/:id` - Partially update a booking (requires authentication)
- **DELETE** `/booking/:id` - Delete a booking (requires authentication)

### Health Check
- **GET** `/ping` - API health check

## Prerequisites

Before running the tests, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/restful-booker-api-tests.git
   cd restful-booker-api-tests
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Tests

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run tests with coverage report
```bash
pytest --cov=. --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_booking.py
```

### Run tests with specific markers (if configured)
```bash
pytest -m smoke
pytest -m regression
```

## Project Structure

```
restful-booker-api-tests/
├── tests/              # Test files
├── utils/              # Helper functions and utilities
├── config/             # Configuration files
├── requirements.txt    # Python dependencies
├── pytest.ini          # Pytest configuration
├── README.md           # This file
└── TEST_CHECKLIST.md   # Detailed test scenarios checklist
```

## Test Reports

After running tests with coverage:
- HTML coverage report: `htmlcov/index.html`
- Open in browser to view detailed coverage

## Configuration

Test configurations can be modified in:
- `pytest.ini` - Pytest settings
- `config/` directory - API endpoints, credentials, etc.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## Notes

- The Restful-Booker API is a public testing API and may occasionally be slow or unavailable
- Authentication credentials: username: `admin`, password: `password123`
- All test data is temporary and will be reset periodically

## Resources

- [Restful-Booker API Documentation](https://restful-booker.herokuapp.com/apidoc/index.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Requests Library Documentation](https://requests.readthedocs.io/)

## License

This project is for educational and testing purposes.
