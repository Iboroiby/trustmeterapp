from fastapi import APIRouter, Depends, Request, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from app.schemas.user import RegisteredUserResponse, RegisterUserInput, LoginUserInput
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import timedelta
from app.services.user_service import user_service
from app.utils.auth import create_access_token, verify_access_token
from app.utils.background_task import send_email_in_background

auth = APIRouter(prefix="/auth", tags=["Authentication"])



@auth.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisteredUserResponse,
)
def register(
    background_tasks: BackgroundTasks,
    user_schema: RegisterUserInput,
    db: Session = Depends(get_db),
):
    """Endpoint for a user to register their account"""

    # Create user account
    user = user_service.create(db=db, schema=user_schema)

    # Create access tokens
    access_token = create_access_token(user_id=str(user.id))

    send_email_in_background(
        background_tasks,
        subject="Welcome to Our App!",
        recipients=[user.email],
        template_name="welcome.html",
        template_context={"name": user.name}
    )

    response = JSONResponse(
        status_code=201,
        content={
            "status_code": 201,
            "message": "User created successfully",
            "access_token": access_token,
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

    access_token = create_access_token(user_id=str(user.id))

    response = JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "User loggedin successfully",
            "access_token": access_token,
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

@auth.get("/me", status_code=status.HTTP_200_OK)
def get_current_user(
    current_user: dict = Depends(verify_access_token),
):
    """Endpoint to get current user details"""

    return JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "User fetched successfully",
            "data": jsonable_encoder(
                    current_user, 
                    exclude=["password", "is_deleted", "updated_at"]
                )
        },
    )
