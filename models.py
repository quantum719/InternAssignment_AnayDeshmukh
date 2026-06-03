from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ════════════════════════════════════════════════════════════════════
# CREATE  schema  — all fields required
# ════════════════════════════════════════════════════════════════════
class EmployeeCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Rahul")
    last_name: str = Field(..., min_length=1, max_length=50, example="Sharma")
    email: EmailStr = Field(..., example="rahul.sharma@company.com")
    phone_number: str = Field(..., min_length=7, max_length=15, example="9876543210")
    department: str = Field(..., min_length=1, max_length=50, example="Engineering")
    designation: str = Field(
        ..., min_length=1, max_length=100, example="Software Engineer"
    )
    salary: float = Field(..., gt=0, example=75000.00)
    joining_date: date = Field(..., example="2022-06-15")


# ════════════════════════════════════════════════════════════════════
# UPDATE  schema  — every field is optional (PATCH-style PUT)
# ════════════════════════════════════════════════════════════════════
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=7, max_length=15)
    department: Optional[str] = Field(None, min_length=1, max_length=50)
    designation: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, gt=0)
    joining_date: Optional[date] = None
