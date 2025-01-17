from passlib.context import CryptContext
import datetime as dt
from app.utils.settings import settings
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str):
    """Hash the password using the bcrypt algorithm"""
    hashed_password = pwd_context.hash(secret=password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str):
    """Verify the password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str):
    """Function to create access token"""

    expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
        days=3
    )
    data = {"user_id": user_id, "exp": expires}
    encoded_jwt = jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_access_token(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Function to decode and token"""
    from app.services.user_service import user_service

    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("user_id")

        user = user_service.get_user_by_id(db, user_id)

        if payload is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError as err:
        print(err)
        raise HTTPException(status_code=401, detail="Error decoding token")

    return user