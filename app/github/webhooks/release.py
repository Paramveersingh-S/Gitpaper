"""
Handle release events.
"""
from app.database import get_db
from app.github.rest import GitHubRestClient
from app.services.report_generator import generate_release_report
from app.github.webhooks.push import get_or_create_repository


async def handle(payload: dict):
    """
    On release published:
    Generate paper coverage report and update release notes.
    """
    action = payload.get("action")
    if action != "published":
        return

    release = payload["release"]
    repo_data = payload["repository"]
    owner = repo_data["owner"]["login"]
    repo_name = repo_data["name"]
    installation_id = payload["installation"]["id"]
    version = release["tag_name"]
    release_id = release["id"]

    client = GitHubRestClient(installation_id)

    async for db in get_db():
        repo = await get_or_create_repository(db, repo_data, installation_id)
        report = await generate_release_report(db, repo.id, version, owner, repo_name)
        
        # Append report to existing release body
        new_body = release.get("body", "") + "\n\n" + report
        await client.create_release_asset_comment(owner, repo_name, release_id, new_body)
