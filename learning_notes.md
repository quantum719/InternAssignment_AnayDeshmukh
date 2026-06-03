# Learning Notes — Assignment 01: Python CRUD API

## About This Document
This file documents my learning journey while building a FastAPI CRUD API
with AI-assisted development using Claude AI.

---

## 1. Key Concepts Learned

### What is a REST API?
- REST (Representational State Transfer) is an architectural style for designing networked applications.
- Uses HTTP methods: GET (read), POST (create), PUT (update), DELETE (delete).
- Resources are represented as URLs (e.g., `/employees`, `/employees/1`).

### Flask vs FastAPI — Why I chose FastAPI
| Feature              | Flask            | FastAPI                        |
|----------------------|------------------|--------------------------------|
| Type hints           | Optional         | Built-in and enforced          |
| Input validation     | Manual           | Automatic via Pydantic         |
| API docs             | Needs extension  | Auto-generated at /docs        |
| Performance          | WSGI (sync)      | ASGI (supports async)          |
| Error messages       | Custom only      | Auto 422 with field details    |

### What is Pydantic?
- A Python library for data validation using type annotations.
- FastAPI uses it to automatically validate request bodies.
- Example: `email: EmailStr` automatically rejects invalid email formats.

### What is Uvicorn?
- An ASGI server that runs FastAPI applications.
- `uvicorn main:app --reload` — `main` is the file, `app` is the FastAPI instance.

---

## 2. Questions Asked to Claude AI & Key Learnings

### Q1: What is the difference between Flask and FastAPI?
**Learning:** FastAPI is built for modern Python. It uses type hints to auto-validate
request data and auto-generates interactive documentation at `/docs`. Flask requires
manual validation and has no built-in docs.

### Q2: How does FastAPI validate request bodies automatically?
**Learning:** FastAPI uses Pydantic `BaseModel` classes. When a route receives a
`POST` request, it automatically parses the JSON body and validates each field against
the Pydantic model. If validation fails, it returns a `422 Unprocessable Entity`
response with specific field-level error messages.

### Q3: What is the `lifespan` parameter in FastAPI?
**Learning:** `lifespan` replaces the deprecated `@app.on_event("startup")` decorator.
It uses a context manager — code before `yield` runs on startup, code after runs on
shutdown. Used here to call `init_db()` when the server starts.

### Q4: What does `model_dump(exclude_unset=True)` do in Pydantic?
**Learning:** When a client sends a `PUT` request with only some fields (e.g., just
`salary`), `exclude_unset=True` returns only the fields that were actually sent,
not all fields with their defaults. This enables partial updates without accidentally
overwriting existing data with `None`.

### Q5: How do I handle MySQL's DECIMAL type in JSON responses?
**Learning:** Python's `mysql-connector` returns `DECIMAL` values as Python `Decimal`
objects, which are not JSON-serialisable by default. The solution is to convert them
to `float` in the helper function before returning the response.

### Q6: What is `HTTPException` in FastAPI?
**Learning:** `HTTPException` is FastAPI's built-in way to return error responses.
`raise HTTPException(status_code=404, detail="Not found")` immediately stops the
route handler and returns a JSON error response with the given status code.

---

## 3. Problems Faced & Resolutions

### Problem 1: JSON serialization error with MySQL DECIMAL type
**Error:** `TypeError: Object of type Decimal is not JSON serializable`
**Cause:** MySQL DECIMAL columns return Python `Decimal` objects, which `json.dumps`
cannot handle by default.
**Resolution:** Created a `_safe()` helper that converts `Decimal` → `float` and
`date` → ISO string before building the response dictionary.

### Problem 2: PUT request was overwriting fields I didn't send
**Cause:** Using `data.model_dump()` (without `exclude_unset=True`) included all
fields with their default `None` values, causing NULL updates in the database.
**Resolution:** Used `data.model_dump(exclude_unset=True)` to only update the
fields the client explicitly sent.

### Problem 3: EmailStr not working / import error
**Cause:** `pydantic[email]` extra was not installed.
**Resolution:** Added `pydantic[email]` to `requirements.txt` and re-ran
`pip install -r requirements.txt`.

---

## 4. Git Workflow Learned

```bash
# Initialise a repository
git init

# Stage and commit
git add .
git commit -m "Initial project setup"

# Connect to GitHub and push
git remote add origin https://github.com/<username>/<repo>.git
git branch -M main
git push -u origin main

# Subsequent pushes
git add .
git commit -m "CRUD APIs implemented"
git push
```

### Good commit message practices
- "Initial project setup — FastAPI + MySQL structure"
- "Database schema and sample data seeding added"
- "All CRUD endpoints implemented"
- "Pydantic validation models added"
- "README and learning notes added"

---

## 5. Tools Used
- **Claude AI** — learning concepts, code generation, debugging
- **FastAPI** — web framework
- **MySQL** — relational database
- **Postman** — API testing
- **Git / GitHub** — version control
