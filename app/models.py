from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from pydantic import BaseModel, Field
from app.database import Base

# --- SQLAlchemy Models ---
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_number = Column(String, index=True)
    to_number = Column(String)
    timestamp = Column(DateTime)
    text = Column(Text)
    ingested_at = Column(DateTime, default=datetime.utcnow)

    # Unique constraint or sufficient indexing for deduplication check.
    # The assignment says "Duplicate: same body and timestamp".
    # Adding an index on (text, timestamp) or individual indices helps.
    # We'll use a manually defined index or just rely on query performance.

# --- Pydantic Schemas ---
class MessageCreate(BaseModel):
    from_number: str = Field(..., alias="from")
    to_number: str = Field(..., alias="to")
    text: str
    timestamp: datetime = Field(..., alias="ts")

    model_config = {
        "populate_by_name": True
    }

class MessageResponse(BaseModel):
    id: int
    from_number: str
    to_number: str
    text: str
    timestamp: datetime
    ingested_at: datetime

    model_config = {
        "from_attributes": True
    }

class PaginatedMessageResponse(BaseModel):
    total: int
    limit: int
    offset: int
    messages: list[MessageResponse]
