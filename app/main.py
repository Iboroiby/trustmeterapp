from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.routes import users

app = FastAPI()

# Include user routes
app.include_router(users.router, prefix="/users", tags=["Users"])

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message":"Welcome to TrustMeter, your go-to platform for trusted reviews!"}