from pydantic import BaseModel, EmailStr, Field

class ContactInfo(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')

class AppointmentDetails(BaseModel):
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    purpose: str = Field(..., min_length=5)
