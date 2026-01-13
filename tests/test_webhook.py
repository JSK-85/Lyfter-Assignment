import pytest
import hmac
import hashlib
import json
from datetime import datetime

from app.config import settings

WEBHOOK_SECRET = settings.WEBHOOK_SECRET

def generate_signature(body_bytes: bytes, secret: str = WEBHOOK_SECRET) -> str:
    return hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()

@pytest.mark.asyncio
async def test_webhook_valid(client):
    payload = {
        "from": "12345",
        "to": "67890",
        "text": "Hello World",
        "ts": datetime.utcnow().isoformat()
    }
    payload_bytes = json.dumps(payload).encode("utf-8")
    headers = {
        "X-Signature": generate_signature(payload_bytes),
        "Content-Type": "application/json"
    }
    
    response = await client.post("/webhook", content=payload_bytes, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_webhook_invalid_signature(client):
    payload = {"from": "123", "to": "456", "text": "Fail", "ts": "now"}
    payload_bytes = json.dumps(payload).encode("utf-8")
    headers = {
        "X-Signature": "invalid",
        "Content-Type": "application/json"
    }
    
    response = await client.post("/webhook", content=payload_bytes, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid signature"

@pytest.mark.asyncio
async def test_webhook_deduplication(client):
    ts = datetime.utcnow().isoformat()
    payload = {
        "from": "111",
        "to": "222",
        "text": "Duplicate Check",
        "ts": ts
    }
    payload_bytes = json.dumps(payload).encode("utf-8")
    headers = {
        "X-Signature": generate_signature(payload_bytes),
        "Content-Type": "application/json"
    }
    
    # First request
    resp1 = await client.post("/webhook", content=payload_bytes, headers=headers)
    assert resp1.status_code == 200
    
    # Second request (duplicate)
    resp2 = await client.post("/webhook", content=payload_bytes, headers=headers)
    assert resp2.status_code == 200
    assert resp2.json().get("info") == "duplicate ignored"
