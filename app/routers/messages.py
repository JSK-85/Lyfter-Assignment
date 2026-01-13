from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import Message, MessageResponse, PaginatedMessageResponse
from app.utils.logger import logger

router = APIRouter()

@router.get("/messages", response_model=PaginatedMessageResponse)
async def get_messages(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_number: Optional[str] = Query(None, alias="from"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve stored messages with pagination.
    """
    # Base query
    query = select(Message)
    
    if from_number:
        query = query.where(Message.from_number == from_number)
    
    # Count total (before pagination)
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Apply pagination and sorting
    query = query.order_by(Message.timestamp.desc()).limit(limit).offset(offset)
    
    result = await db.execute(query)
    messages = result.scalars().all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "messages": messages
    }
