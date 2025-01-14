from fastapi import FastAPI
<<<<<<< HEAD
from app.db.base import Base
from app.db.session import engine
from app.api.routes import users
=======
import uvicorn
from app.utils.settings import settings
>>>>>>> 4a4b6679d2dfaa9c13514ce2eaec75396c843031

app = FastAPI()

# Include user routes
app.include_router(users.router, prefix="/users", tags=["Users"])

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
<<<<<<< HEAD
async def root():
    return {"message":"Welcome to TrustMeter, your go-to platform for trusted reviews!"}
=======
def read_root():
    return {"message": "Welcome to Trustmeter!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
>>>>>>> 4a4b6679d2dfaa9c13514ce2eaec75396c843031
