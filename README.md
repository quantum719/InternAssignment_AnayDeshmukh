# Employee Management API

A RESTful CRUD API built with **FastAPI** and **MySQL** for managing employee records.

---

## Tech Stack

| Layer     | Technology                |
|-----------|---------------------------|
| Language  | Python 3.10+              |
| Framework | FastAPI                   |
| Database  | MySQL                     |
| Server    | Uvicorn (ASGI)            |

---

## Project Structure

```
employee_api/
├── main.py           # FastAPI app + all route handlers
├── database.py       # MySQL connection & table initialisation
├── models.py         # Pydantic request/validation schemas
├── requirements.txt  # Python dependencies
├── .env.example      # Template for environment variables
├── .gitignore
├── README.md
└── learning_notes.md
```

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/InternAssignment_<YourName>.git
cd InternAssignment_<YourName>
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Open .env and fill in your MySQL credentials
```

**.env file:**
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=employee_db
```

### 5. Create the MySQL database
```sql
CREATE DATABASE employee_db;
```
The table and sample data are created automatically on first run.

### 6. Start the server
```bash
uvicorn main:app --reload
```

The API will be live at **http://127.0.0.1:8000**

Interactive docs: **http://127.0.0.1:8000/docs** (Swagger UI)

---

## API Endpoints

| Method | Endpoint                  | Description            |
|--------|---------------------------|------------------------|
| GET    | `/employees`              | Get all employees      |
| GET    | `/employees/{id}`         | Get employee by ID     |
| POST   | `/employees`              | Create a new employee  |
| PUT    | `/employees/{id}`         | Update an employee     |
| DELETE | `/employees/{id}`         | Delete an employee     |

---

## Sample Requests & Responses

### GET /employees
```http
GET http://127.0.0.1:8000/employees
```
**Response 200:**
```json
{
  "status": "success",
  "count": 2,
  "employees": [
    {
      "employee_id": 1,
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul.sharma@company.com",
      "phone_number": "9876543210",
      "department": "Engineering",
      "designation": "Software Engineer",
      "salary": 75000.0,
      "joining_date": "2022-06-15"
    }
  ]
}
```

---

### GET /employees/{id}
```http
GET http://127.0.0.1:8000/employees/1
```
**Response 200:**
```json
{
  "status": "success",
  "employee": {
    "employee_id": 1,
    "first_name": "Rahul",
    "last_name": "Sharma",
    "email": "rahul.sharma@company.com",
    "phone_number": "9876543210",
    "department": "Engineering",
    "designation": "Software Engineer",
    "salary": 75000.0,
    "joining_date": "2022-06-15"
  }
}
```
**Response 404 (not found):**
```json
{
  "detail": "Employee with ID 99 not found"
}
```

---

### POST /employees
```http
POST http://127.0.0.1:8000/employees
Content-Type: application/json

{
  "first_name": "Arjun",
  "last_name": "Nair",
  "email": "arjun.nair@company.com",
  "phone_number": "9000012345",
  "department": "Engineering",
  "designation": "Backend Developer",
  "salary": 82000,
  "joining_date": "2024-07-01"
}
```
**Response 201:**
```json
{
  "status": "success",
  "message": "Employee created successfully",
  "employee": {
    "employee_id": 6,
    "first_name": "Arjun",
    "last_name": "Nair",
    "email": "arjun.nair@company.com",
    "phone_number": "9000012345",
    "department": "Engineering",
    "designation": "Backend Developer",
    "salary": 82000.0,
    "joining_date": "2024-07-01"
  }
}
```
**Response 409 (duplicate email):**
```json
{
  "detail": "Email already exists. Each employee must have a unique email."
}
```
**Response 422 (validation error):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

### PUT /employees/{id}
```http
PUT http://127.0.0.1:8000/employees/6
Content-Type: application/json

{
  "salary": 90000,
  "designation": "Senior Backend Developer"
}
```
**Response 200:**
```json
{
  "status": "success",
  "message": "Employee updated successfully",
  "employee": {
    "employee_id": 6,
    "first_name": "Arjun",
    "last_name": "Nair",
    "email": "arjun.nair@company.com",
    "phone_number": "9000012345",
    "department": "Engineering",
    "designation": "Senior Backend Developer",
    "salary": 90000.0,
    "joining_date": "2024-07-01"
  }
}
```

---

### DELETE /employees/{id}
```http
DELETE http://127.0.0.1:8000/employees/6
```
**Response 200:**
```json
{
  "status": "success",
  "message": "Employee with ID 6 deleted successfully"
}
```

---

## HTTP Status Codes Used

| Code | Meaning                        |
|------|--------------------------------|
| 200  | OK — request succeeded         |
| 201  | Created — new record added     |
| 400  | Bad Request — no fields to update |
| 404  | Not Found — employee ID doesn't exist |
| 409  | Conflict — duplicate email     |
| 422  | Unprocessable Entity — validation failed |
