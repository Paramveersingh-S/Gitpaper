"""
Handle push events.
On every push, scan commit messages for [eq:X] and [algo:X] tags.
Store these as equation_mappings in the database.
"""
from app.database import get_db
from app.models.equation_mapping import EquationMapping
from app.models.repository import Repository
from app.services.config_parser import fetch_and_parse_gitpaper_config
from app.github.rest import GitHubRestClient
from app.services.commit_tagger import EQUATION_TAG_PATTERN, extract_tag_description
from sqlalchemy import select


async def get_or_create_repository(db, repo_data: dict, installation_id: int) -> Repository:
    repo_id = repo_data["id"]
    result = await db.execute(select(Repository).filter(Repository.id == repo_id))
    repo = result.scalars().first()
    if not repo:
        repo = Repository(
            id=repo_id,
            installation_id=installation_id,
            owner=repo_data["owner"]["login"],
            name=repo_data["name"]
        )
        db.add(repo)
        await db.flush()
    return repo


async def handle(payload: dict):
    """
    Process a push event.
    """
    repo_data = payload.get("repository", {})
    owner = repo_data["owner"]["login"]
    repo_name = repo_data["name"]
    installation_id = payload["installation"]["id"]
    commits = payload.get("commits", [])

    client = GitHubRestClient(installation_id)

    async for db in get_db():
        repo = await get_or_create_repository(db, repo_data, installation_id)

        for commit in commits:
            sha = commit["sha"]
            message = commit.get("message", "")
            modified_files = commit.get("modified", []) + commit.get("added", [])

            tags = EQUATION_TAG_PATTERN.findall(message)
            for tag_type, tag_value in tags:
                equation_label = f"{tag_type}:{tag_value}"

                for file_path in modified_files:
                    mapping = EquationMapping(
                        repository_id=repo.id,
                        paper_id=1,  # Placeholder, in real world we need to resolve the paper based on config
                        commit_sha=sha,
                        file_path=file_path,
                        equation_label=equation_label,
                        description=extract_tag_description(message, equation_label),
                    )
                    db.add(mapping)

            if ".gitpaper.yml" in modified_files:
                await fetch_and_parse_gitpaper_config(
                    db=db,
                    client=client,
                    owner=owner,
                    repo_name=repo_name,
                    repo_id=repo.id,
                    ref=sha
                )

        db.commit()
