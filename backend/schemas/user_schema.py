from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., max_length=50 ,description="User first name")
    last_name: str = Field(..., max_length=50, description="User last name")
    password: str = Field(..., min_length=8, description="User password")
    birth_date: date = Field(..., description="User birth date")
    role: str = Field(..., description="User role")

class UserBase(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    birth_date: date
    role: str