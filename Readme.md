# Expense Tracker API

A RESTful API built with FastAPI and PostgreSQL to track and manage personal expenses.

This project allows users to record daily expenses, categorize them, view summaries (total, monthly, highest expense, and category-wise), export records to CSV or JSON, and send email reports.

---

## What I Used in This Project

Here are the main tools and Python libraries used:

- Python 3.12
- FastAPI: The web framework used to build all the REST API endpoints and auto-generate interactive API documentation.
- PostgreSQL: The relational database used to store expense records.
- SQLAlchemy 2.0: Object Relational Mapper (ORM) used to define database models and run SQL queries using Python code.
- Psycopg (psycopg 3): The database driver that connects SQLAlchemy to PostgreSQL.
- Pydantic: Used for request validation and response schemas, ensuring input data like amount and date are properly formatted.
- Python-dotenv: Used to read secret keys and database settings from a `.env` file instead of hardcoding them.
- Smtplib and EmailMessage: Python built-in libraries used to connect to an SMTP mail server and send expense summary emails.
- CSV and JSON: Python built-in modules used to generate downloadable expense reports in CSV and JSON formats.
- Uvicorn: ASGI web server used to run the FastAPI application locally.
- uv: Fast Python package and project manager used for dependency management.

---

## Project Structure

```text
expense_tracker/
|-- app/
|   |-- database.py              # Database connection and session setup
|   |-- main.py                  # FastAPI app entry point and router registration
|   |-- enums/
|   |   `-- expense_category.py  # Category choices (food, travel, bills, etc.)
|   |-- models/
|   |   `-- expense.py           # SQLAlchemy Expense database model
|   |-- routers/
|   |   |-- categories.py        # Category-related endpoints
|   |   |-- expenses.py          # CRUD endpoints for expenses
|   |   |-- exports.py           # CSV and JSON export endpoints
|   |   |-- reports.py           # Email report endpoint
|   |   `-- summaries.py         # Spending summary and analytics endpoints
|   |-- schemas/
|   |   |-- expense.py           # Pydantic validation schemas (Create, Update, Response)
|   |   `-- summary.py           # Pydantic schemas for summary responses
|   |-- services/
|   |   |-- email_service.py     # Logic to send emails using smtplib
|   |   |-- expense_service.py   # Database queries for expense CRUD operations
|   |   |-- export_service.py    # CSV and JSON stream generation
|   |   `-- summary_service.py   # Aggregation queries for totals and monthly stats
|   `-- utils/
|       `-- exceptions.py        # Reusable HTTP exception helpers
|-- .env                         # Environment variables (Not committed here)
|-- pyproject.toml               # Project dependencies and metadata
`-- Readme.md                    # Project documentation
```

---

## Environment Variables (.env)

The application uses a `.env` file in the `expense_tracker` root directory to store configuration settings.

Create a file named `.env` in the `expense_tracker` folder with the following variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/expenses
PORT=8000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Explanation of Variables

1. `DATABASE_URL`:
   The PostgreSQL connection string. Format:
   `postgresql+psycopg://<username>:<password>@<host>:<port>/<database_name>`
   Example: `postgresql+psycopg://postgres:postgres@localhost:5432/expenses`

2. `PORT`:
   The port number on which the FastAPI application will run (default is `8000`).

3. `SMTP_HOST`:
   The mail server address used for sending email reports. For Gmail, use `smtp.gmail.com`.

4. `SMTP_PORT`:
   The mail server port number. For Gmail with TLS, use `587`.

5. `SMTP_USERNAME`:
   The email address used to send reports (e.g., your Gmail address).

6. `SMTP_PASSWORD`:
   The password or App Password for your email account.
   If using Gmail, regular account passwords will not work because of security policies. You must generate a Google App Password:
   - Go to your Google Account settings.
   - Go to Security and turn on 2-Step Verification if it is not enabled.
   - Search for "App Passwords" in the search bar.
   - Create a new App Password (name it something like "Expense Tracker").
   - Copy the 16-character generated password and paste it as `SMTP_PASSWORD` without spaces.

---

## How to Set Up and Run the Project

Follow these steps to run the application on your computer:

### Step 1: Clone or Open the Project

Open a terminal and navigate to the project directory:

```bash
cd "d:/Projects Python/FastAPI/expense_tracker"
```

### Step 2: Set Up PostgreSQL Database

Make sure PostgreSQL is installed and running on your system.

Open PostgreSQL command line (psql) or pgAdmin, and create a database named `expenses`:

```sql
CREATE DATABASE expenses;
```

Tables will be created automatically when the FastAPI application starts because `Base.metadata.create_all(bind=engine)` is called in `app/main.py`.

### Step 3: Configure Environment Variables

Create the `.env` file inside the `expense_tracker` folder (you can copy `.env.example`) and fill in your database credentials and email settings as explained above:

```bash
# On Windows PowerShell:
cp .env.example .env
```

### Step 4: Install Dependencies

If you are using `uv`:

```bash
uv sync
```

Or if you are using standard Python with a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.venv\Scripts\activate.bat
# On macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### Step 5: Run the Server

Using `uv`:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Or using standard uvicorn with your activated virtual environment:

```bash
uvicorn app.main:app --reload --port 8000
```

The application will start running at:
`http://127.0.0.1:8000`

### Step 6: Test the API with Swagger Docs

FastAPI comes with automatic documentation. Open your browser and visit:

- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Alternative ReDoc UI: `http://127.0.0.1:8000/redoc`

You can test all endpoints directly from the Swagger UI interface.

---

## API Endpoints

### 1. Expenses (`/api/expenses`)

- `POST /api/expenses/`
  Creates a new expense.
  Example request body:
  ```json
  {
    "title": "Grocery Shopping",
    "amount": 45.50,
    "description": "Vegetables and fruits",
    "category": "food",
    "expense_date": "2026-09-13"
  }
  ```

- `GET /api/expenses/`
  Returns all active expenses, sorted by date (newest first).

- `GET /api/expenses/{expense_id}`
  Returns a specific expense by its UUID.

- `PUT /api/expenses/{expense_id}`
  Updates an existing expense by its UUID. You can update any fields (title, amount, description, category, expense_date).

- `DELETE /api/expenses/{expense_id}`
  Soft-deletes an expense by its UUID (sets `is_active = False` in the database). Returns HTTP status 204.

---

### 2. Categories (`/api`)

- `GET /api/categories`
  Returns a list of all distinct categories that currently have active expenses.

- `GET /api/expenses/category/{category}`
  Returns all active expenses belonging to a specific category.
  Available categories:
  - `food`
  - `travel`
  - `shopping`
  - `bills`
  - `entertainment`
  - `health`
  - `education`
  - `other`

---

### 3. Summaries and Analytics (`/api/expenses/summary`)

- `GET /api/expenses/summary/total`
  Returns the total spending amount across all active expenses.

- `GET /api/expenses/summary/monthly`
  Returns monthly spending grouped by year and month.
  Example response:
  ```json
  [
    {
      "year": 2026,
      "month": 9,
      "total_spending": 250.75
    }
  ]
  ```

- `GET /api/expenses/summary/highest`
  Returns the single expense with the highest amount.

- `GET /api/expenses/summary/category`
  Returns total spending grouped by category, ordered from highest spending to lowest.

---

### 4. Data Exports (`/api/expenses/export`)

- `GET /api/expenses/export/csv`
  Downloads all active expenses as a CSV file (`expenses.csv`).

- `GET /api/expenses/export/json`
  Downloads all active expenses as a JSON file (`expenses.json`).

---

### 5. Email Reports (`/api/expenses/report`)

- `POST /api/expenses/report/email/{email_id}/`
  Generates a text-based summary of total spending and the latest expenses, and sends it to the provided email address using SMTP.

---

## Notes for Beginners

- When deleting an expense, it is not permanently erased from the database; it uses soft deletion (`is_active = False`).
- Make sure not to share your `.env` file or commit it to GitHub to keep your database password and email app password safe.
- Dates must be formatted as `YYYY-MM-DD`.
- UUIDs are required for single expense operations (such as `GET`, `PUT`, `DELETE`). You can find the UUID from the response of `POST /api/expenses/` or `GET /api/expenses/`.
