from sqlalchemy.orm import Session
from app.schemas.user import RegisterUserInput, LoginUserInput
from app.models.user import User
from fastapi import HTTPException
from app.utils.auth import hash_password, verify_password

class UserService:
    """ User service class """
    def create(self, db: Session, schema: RegisterUserInput):
        """Create a new user account"""
        if db.query(User).filter(User.email == schema.email).first():
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists",
            )
        schema.password = hash_password(password=schema.password)
        user = User(**schema.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    def login_user(self, db: Session, schema: LoginUserInput):
        """Login a user"""
        user = db.query(User).filter(User.email == schema.email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Incorrect email or password",
            )
        if not verify_password(plain_password=schema.password, hashed_password=user.password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password",
            )
        return user

user_service = UserService()
