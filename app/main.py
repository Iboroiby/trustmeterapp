 # app/main.py
from fastapi import FastAPI
import uvicorn
from app.utils.settings import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Trustmeter!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
