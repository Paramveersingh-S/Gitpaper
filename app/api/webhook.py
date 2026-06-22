"""
Main webhook endpoint. GitHub sends all events here.
This is the heart of the GitHub App.
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from app.config import settings
from app.utils.crypto import require_valid_signature
from app.github.webhooks import push, pull_request, release, installation as install_handler
import json

router = APIRouter()


@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    Receive and route GitHub webhook events.
    """
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")
    require_valid_signature(body, signature, settings.github_webhook_secret)

    event_type = request.headers.get("X-GitHub-Event", "")
    delivery_id = request.headers.get("X-GitHub-Delivery", "")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    handlers = {
        "push": push.handle,
        "pull_request": pull_request.handle,
        "release": release.handle,
        "installation": install_handler.handle,
        "installation_repositories": install_handler.handle_repositories,
    }

    handler = handlers.get(event_type)
    if handler:
        import asyncio
        asyncio.create_task(handler(payload))

    return {"status": "accepted", "event": event_type, "delivery_id": delivery_id}
