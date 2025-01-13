 # app/main.py
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from app.utils.settings import settings
from app.db.database import engine, Base, get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Trustmeter!"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Create a new user
    new_user = User(id=user.id, name=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
