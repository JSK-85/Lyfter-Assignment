from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Message, MessageCreate
from app.utils.security import validate_signature
from app.utils.logger import logger

router = APIRouter()

@router.post("/webhook", status_code=status.HTTP_200_OK, dependencies=[Depends(validate_signature)])
async def receive_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    """
    Ingest a new message.
    """
    # Deduplication check: Same body and timestamp
    query = select(Message).where(
        Message.text == message.text,
        Message.timestamp == message.timestamp
    )
    result = await db.execute(query)
    existing_message = result.scalar_one_or_none()

    if existing_message:
        logger.info(f"Duplicate message received: {message}")
        return {"status": "ok", "info": "duplicate ignored"}

    new_message = Message(
        from_number=message.from_number,
        to_number=message.to_number,
        text=message.text,
        timestamp=message.timestamp
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    logger.info(f"Message ingested: {new_message.id}")
    return {"status": "ok"}
