import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_messages_api(client):
    # Retrieve empty list first
    resp = await client.get("/messages")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0

    # Insert a message (assume webhook works or bypass it later, but here we use webhook)
    # We depend on the previous tests passing or just running this isolated
    # But integration tests are better.
    # Let's insert via webhook helper
    import hmac, hashlib, json
    from app.config import settings
    
    def sign(b):
        return hmac.new(settings.WEBHOOK_SECRET.encode("utf-8"), b, hashlib.sha256).hexdigest()

    payload = {"from": "999", "to": "888", "text": "Test Msg", "ts": datetime.utcnow().isoformat()}
    payload_bytes = json.dumps(payload).encode("utf-8")
    headers = {
        "X-Signature": sign(payload_bytes),
        "Content-Type": "application/json"
    }
    await client.post("/webhook", content=payload_bytes, headers=headers)

    # Fetch again
    resp = await client.get("/messages")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["messages"][0]["text"] == "Test Msg"
