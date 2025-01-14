from passlib.context import CryptContext
import datetime as dt
from app.utils.settings import settings
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    data = {"user_id": user_id, "exp": expires, "type": "refresh"}
    encoded_jwt = jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return encoded_jwt