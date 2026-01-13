from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter()

@router.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "ok"}
