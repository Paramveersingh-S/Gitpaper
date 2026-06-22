"""
Handle installation events.
"""
from app.database import get_db
from app.models.installation import Installation
from sqlalchemy import select


async def handle(payload: dict):
    """
    Handle app installation and uninstallation.
    """
    action = payload.get("action")
    installation_data = payload["installation"]
    installation_id = installation_data["id"]

    async for db in get_db():
        if action == "created":
            inst = Installation(
                installation_id=installation_id,
                account_login=installation_data["account"]["login"],
                account_type=installation_data["account"]["type"],
                access_tokens_url=installation_data["access_tokens_url"],
                is_active=True
            )
            db.add(inst)
            db.commit()
        elif action == "deleted":
            result = await db.execute(select(Installation).where(Installation.installation_id == installation_id))
            inst = result.scalars().first()
            if inst:
                inst.is_active = False
                db.commit()


async def handle_repositories(payload: dict):
    """
    Handle when repositories are added or removed from an installation.
    """
    # implementation omitted for brevity, logic would parse added/removed repos
    pass
