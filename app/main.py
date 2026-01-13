from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from app.config import settings
from app.database import engine, Base
from app.routers import webhook, messages, health, stats
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")
    yield
    # Shutdown logic if needed

app = FastAPI(title="Lyftr AI Backend Assignment", lifespan=lifespan)

# Setup Metrics
Instrumentator().instrument(app).expose(app)

# Include Routers
app.include_router(webhook.router)
app.include_router(messages.router)
app.include_router(health.router)
app.include_router(stats.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
