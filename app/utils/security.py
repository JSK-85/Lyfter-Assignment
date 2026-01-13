import hmac
import hashlib
from fastapi import Request, HTTPException, status
from app.config import settings
from app.utils.logger import logger

async def validate_signature(request: Request):
    """
    Validates the X-Signature header using HMAC-SHA256.
    """
    signature = request.headers.get("X-Signature")
    if not signature:
        logger.warning("Missing X-Signature header")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-Signature header")

    body = await request.body()
    secret = settings.WEBHOOK_SECRET.encode("utf-8")
    
    # Calculate expected signature
    expected_signature = hmac.new(secret, body, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(expected_signature, signature):
        logger.warning("Invalid signature")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    
    return True
