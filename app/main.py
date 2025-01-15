from fastapi import FastAPI
from app.api.routes import users
import uvicorn
from app.utils.settings import settings
from app.api.routes import api_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Trustmeter!"}

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
