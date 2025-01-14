from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from app.schemas.user import RegisteredUserResponse, RegisterUserInput, LoginUserInput
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import timedelta
from app.services.user_service import user_service
from app.utils.auth import create_access_token

auth = APIRouter(prefix="/auth", tags=["Authentication"])

@auth.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisteredUserResponse,
)
def register(
    request: Request,
    user_schema: RegisterUserInput,
    db: Session = Depends(get_db),
):
    """Endpoint for a user to register their account"""

    # Create user account
    user = user_service.create(db=db, schema=user_schema)

    # Create access tokens
    access_token = create_access_token(user_id=str(user.id))

    response = JSONResponse(
        status_code=201,
        content={
            "status_code": 201,
            "message": "User created successfully",
            "access_token": access_token,
            "refresh_token": "refresh_token",
            "data": jsonable_encoder(
                    user, 
                    exclude=["password", "is_deleted", "updated_at"]
                )
        },
    )

    # Add token to cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        expires=timedelta(days=60),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response

@auth.post(
    "/login", status_code=status.HTTP_200_OK, response_model=RegisteredUserResponse
)
def login(login_schema: LoginUserInput, request: Request, db: Session = Depends(get_db)):
    """Endpoint to log in a user"""

    user = user_service.login_user(
        db=db, schema=login_schema)

    # Generate access tokens
    access_token = create_access_token(user_id=str(user.id))

    response = JSONResponse(
        status_code=201,
        content={
            "status_code": 201,
            "message": "User loggedin successfully",
            "access_token": access_token,
            "refresh_token": "refresh_token",
            "data": jsonable_encoder(
                    user, 
                    exclude=["password", "is_deleted", "updated_at"]
                )
        },
    )

    # Add access token to cookies
    response.set_cookie(
        key="acess_token",
        value=access_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response