import pytest
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_stats_endpoint(client):
    # Check initial stats
    resp = await client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_messages"] == 0
    assert data["messages_last_24h"] == 0

    # Insert a message (using webhook helper or direct DB if possible, but let's stick to webhook pattern if we can sign it easily, or just assume previous tests passed and use the client)
    # We need to sign it.
    import hmac, hashlib, json
    from app.config import settings
    
    def sign(b):
        return hmac.new(settings.WEBHOOK_SECRET.encode("utf-8"), b, hashlib.sha256).hexdigest()

    payload = {"from": "stats_user", "to": "123", "text": "Stats Test", "ts": datetime.utcnow().isoformat()}
    payload_bytes = json.dumps(payload).encode("utf-8")
    headers = {"X-Signature": sign(payload_bytes), "Content-Type": "application/json"}
    
    await client.post("/webhook", content=payload_bytes, headers=headers)

    # Check stats update
    resp = await client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_messages"] == 1
    assert data["messages_last_24h"] == 1
    assert data["top_sender"]["number"] == "stats_user"
