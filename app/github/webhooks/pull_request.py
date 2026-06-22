"""
Handle pull_request events.
"""
from app.database import get_db
from app.models.equation_mapping import EquationMapping
from app.models.paper import Paper
from app.github.rest import GitHubRestClient
from app.services.drift_detector import build_drift_comment
from sqlalchemy import select


async def handle(payload: dict):
    """
    On PR opened or updated:
    1. Get list of files changed in the PR
    2. Look up which equations those files implement
    3. If any matches found, post a drift warning comment
    """
    action = payload.get("action")
    if action not in ("opened", "synchronize", "reopened"):
        return

    pr = payload["pull_request"]
    pr_number = pr["number"]
    repo_data = payload["repository"]
    owner = repo_data["owner"]["login"]
    repo_name = repo_data["name"]
    installation_id = payload["installation"]["id"]
    pr_author = pr["user"]["login"]

    client = GitHubRestClient(installation_id)

    changed_files = await client.get_pull_request_files(owner, repo_name, pr_number)
    changed_file_paths = [f["filename"] for f in changed_files]

    async for db in get_db():
        result = await db.execute(
            select(EquationMapping, Paper)
            .join(Paper, EquationMapping.paper_id == Paper.id, isouter=True)
            .where(EquationMapping.file_path.in_(changed_file_paths))
        )
        mappings = result.fetchall()

        if not mappings:
            return

        comment = build_drift_comment(mappings, pr_author)
        await client.create_pr_comment(owner, repo_name, pr_number, comment)
