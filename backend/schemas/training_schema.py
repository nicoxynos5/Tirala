from pydantic import BaseModel, EmailStr, Field
from datetime import date

class Training25Shots(BaseModel):
    user_id: int
    successful_shots: int
    corner_left: int
    corner_right: int
    wing_left: int
    wing_right: int
    top_key: int
    notes: str