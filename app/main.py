from fastapi import FastAPI, Request
from app.api.routes import users
import uvicorn
from app.utils.settings import settings
from app.api.routes import api_router
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Trustmeter!"}

app.include_router(api_router)

# Error Handlers 
@app.exception_handler(HTTPException)
async def http_exception(request: Request, exc: HTTPException):
    """HTTP exception handler"""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception(request: Request, exc: RequestValidationError):
    """Validation exception handler"""

    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "status_code": 422,
            "message": "Invalid input",
            "errors": errors,
        },
    )

@app.exception_handler(IntegrityError)
async def integrity_exception(request: Request, exc: IntegrityError):
    """Integrity error exception handlers"""

    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "status_code": 500,
            "message": f"An unexpected error occurred: {exc}",
        },
    )
@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    """Other exception handlers"""

    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "status_code": 500,
            "message": f"An unexpected error occurred: {exc}",
        },
    )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
