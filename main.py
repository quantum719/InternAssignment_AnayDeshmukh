from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from decimal import Decimal
from datetime import date

from database import get_connection, init_db
from models import EmployeeCreate, EmployeeUpdate

import mysql.connector


# ─── Startup: initialise the DB before accepting requests ───────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Employee Management API",
    description="A CRUD REST API for managing employee records (FastAPI + MySQL)",
    version="1.0.0",
    lifespan=lifespan,
)


# ─── Helper: convert a cursor row to a JSON-safe dict ───────────────
def _safe(v):
    """Convert MySQL types that are not JSON-serialisable."""
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, date):
        return v.isoformat()
    return v

def rows_to_list(cursor) -> list[dict]:
    columns = [col[0] for col in cursor.description]
    return [{k: _safe(v) for k, v in zip(columns, row)} for row in cursor.fetchall()]

def row_to_dict(cursor, row) -> dict:
    columns = [col[0] for col in cursor.description]
    return {k: _safe(v) for k, v in zip(columns, row)}


# ════════════════════════════════════════════════════════════════════
# READ ALL   GET /employees
# ════════════════════════════════════════════════════════════════════
@app.get("/employees", summary="Get all employees")
def get_all_employees():
    """Return every employee record in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = rows_to_list(cursor)
    cursor.close()
    conn.close()

    return {
        "status":    "success",
        "count":     len(employees),
        "employees": employees,
    }


# ════════════════════════════════════════════════════════════════════
# READ ONE   GET /employees/{employee_id}
# ════════════════════════════════════════════════════════════════════
@app.get("/employees/{employee_id}", summary="Get employee by ID")
def get_employee(employee_id: int):
    """Return a single employee by their integer ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    row = cursor.fetchone()

    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found",
        )

    employee = row_to_dict(cursor, row)
    cursor.close()
    conn.close()

    return {"status": "success", "employee": employee}


# ════════════════════════════════════════════════════════════════════
# CREATE     POST /employees
# ════════════════════════════════════════════════════════════════════
@app.post("/employees", status_code=201, summary="Create a new employee")
def create_employee(data: EmployeeCreate):
    """
    Add a new employee record.
    All fields are required. Email must be unique.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO employees
                (first_name, last_name, email, phone_number,
                 department, designation, salary, joining_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.first_name,
                data.last_name,
                data.email,
                data.phone_number,
                data.department,
                data.designation,
                data.salary,
                data.joining_date,   # Pydantic already validated as date
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid

    except mysql.connector.IntegrityError:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Email already exists. Each employee must have a unique email.",
        )

    # Fetch and return the newly created record
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (new_id,))
    new_employee = row_to_dict(cursor, cursor.fetchone())
    cursor.close()
    conn.close()

    return {
        "status":   "success",
        "message":  "Employee created successfully",
        "employee": new_employee,
    }


# ════════════════════════════════════════════════════════════════════
# UPDATE     PUT /employees/{employee_id}
# ════════════════════════════════════════════════════════════════════
@app.put("/employees/{employee_id}", summary="Update an existing employee")
def update_employee(employee_id: int, data: EmployeeUpdate):
    """
    Partially update an employee.
    Only send the fields you want to change — all fields are optional.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Confirm employee exists before attempting the update
    cursor.execute("SELECT employee_id FROM employees WHERE employee_id = %s", (employee_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found",
        )

    # exclude_unset=True means only fields the client actually sent are included
    updates = data.model_dump(exclude_unset=True)

    if not updates:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="No valid fields provided to update.",
        )

    set_clause = ", ".join(f"{col} = %s" for col in updates)
    values     = list(updates.values()) + [employee_id]

    try:
        cursor.execute(
            f"UPDATE employees SET {set_clause} WHERE employee_id = %s",
            values,
        )
        conn.commit()
    except mysql.connector.IntegrityError:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Email already exists. Each employee must have a unique email.",
        )

    # Fetch and return the updated record
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    updated_employee = row_to_dict(cursor, cursor.fetchone())
    cursor.close()
    conn.close()

    return {
        "status":   "success",
        "message":  "Employee updated successfully",
        "employee": updated_employee,
    }


# ════════════════════════════════════════════════════════════════════
# DELETE     DELETE /employees/{employee_id}
# ════════════════════════════════════════════════════════════════════
@app.delete("/employees/{employee_id}", summary="Delete an employee")
def delete_employee(employee_id: int):
    """Permanently remove an employee record by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT employee_id FROM employees WHERE employee_id = %s", (employee_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found",
        )

    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "status":  "success",
        "message": f"Employee with ID {employee_id} deleted successfully",
    }
