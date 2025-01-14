from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Hash the password using the bcrypt algorithm"""
    hashed_password = pwd_context.hash(secret=password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str):
    """Verify the password"""
    return pwd_context.verify(plain_password, hashed_password)