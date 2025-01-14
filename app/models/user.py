from sqlalchemy import Column, Integer, String, Boolean
from app.models.baseModel import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)