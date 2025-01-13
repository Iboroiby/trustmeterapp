from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    id: str
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
