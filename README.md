# Finance Dashboard API

## Description
This project is a high-performance backend for a finance dashboard, built with FastAPI. It provides a robust set of features for user management, role-based access control, financial records management, and detailed dashboard analytics. The application uses PostgreSQL for data persistence and SQLAlchemy for ORM, ensuring data integrity and efficient querying.

## Features
- **Role-Based Access Control (RBAC)**: Supports roles such as ADMIN, ANALYST, and VIEWER to manage permissions effectively.
- **User and Role Management**: Comprehensive management of users, including authentication and soft deletion.
- **Financial Records Management**: CRUD operations for financial records with advanced filtering by type, category, and date range.
- **Dashboard Analytics**:
    - **Summary Statistics**: Real-time balance calculations using database aggregations.
    - **Category Breakdown**: Grouped analysis of spending patterns.
    - **Weekly Trends**: Analysis of income and expenses over time.
- **JWT Authentication**: Secure and stateless session management using JSON Web Tokens.
- **Database Migrations**: Managed via Alembic for version-controlled schema evolution.
- **Testing Suite**: Includes unit and integration tests using pytest to ensure system reliability.

## Technology Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migration Tool**: Alembic
- **Authentication**: PyJWT
- **Data Validation**: Pydantic
- **Testing**: pytest
- **Environment Management**: python-dotenv

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- PostgreSQL database

### Step 1: Clone the repository
```bash
git clone https://github.com/singhakshitraj/fin-dash.git
cd fin-dashboard
```

### Step 2: Set up a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate  # On Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables
Create a `.env` file in the root directory and add the following:
```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=<your_secret_key>
ALGORITHM=HS256
ADMIN_USERNAME=admin
```

### Step 5: Run database migrations
```bash
alembic upgrade head
```

## Running the Application
To start the FastAPI development server, run:
```bash
uvicorn main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

## API Documentation
Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing
To run the testing suite, use:
```bash
pytest tests/
```
This will automatically detect all the test files recursively and give the results. Tests are categorized into `tests/unit/` for discrete logic and `tests/integration/` for end-to-end functionality.

## Project Structure
```text
fin-dashboard/
├── alembic/            # Database migration scripts
├── auth/               # Authentication and JWT logic
├── db/                 # Database models, schemas, and connection
├── routers/            # API endpoints for users, records, and dashboard
├── tests/              # Unit and integration test suites
├── utils/              # Utility functions and helpers
├── main.py             # Application entry point
├── alembic.ini         # Alembic configuration
├── requirements.txt    # Project dependencies
└── .env                # Environment configuration
```
