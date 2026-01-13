from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Message
from app.utils.logger import logger

router = APIRouter()

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    Get simple message analytics.
    """
    # Total messages
    total_query = select(func.count()).select_from(Message)
    total = (await db.execute(total_query)).scalar_one()

    # Messages in last 24h
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    recent_query = select(func.count()).select_from(Message).where(Message.timestamp >= one_day_ago)
    recent = (await db.execute(recent_query)).scalar_one()

    # Top sender (simple)
    # SQLite might need specific syntax for grouping, but basic group by is standard
    top_sender_query = (
        select(Message.from_number, func.count(Message.id).label("count"))
        .group_by(Message.from_number)
        .order_by(func.count(Message.id).desc())
        .limit(1)
    )
    top_sender_result = (await db.execute(top_sender_query)).first()
    
    top_sender = None
    if top_sender_result:
        top_sender = {"number": top_sender_result[0], "count": top_sender_result[1]}

    return {
        "total_messages": total,
        "messages_last_24h": recent,
        "top_sender": top_sender,
        "generated_at": datetime.utcnow()
    }
