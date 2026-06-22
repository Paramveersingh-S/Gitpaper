"""
Parse .gitpaper.yml configuration files.
"""
import yaml
from typing import Optional
from app.github.rest import GitHubRestClient
from app.services.paper_fetcher import fetch_arxiv_paper
from app.models.paper import Paper


async def fetch_and_parse_gitpaper_config(
    db,
    client: GitHubRestClient,
    owner: str,
    repo_name: str,
    repo_id: int,
    ref: str = "main"
) -> Optional[dict]:
    """
    Fetch .gitpaper.yml from repo and process all linked papers.
    Called on: installation, push to .gitpaper.yml, first setup.
    """
    content = await client.get_file_content(owner, repo_name, ".gitpaper.yml", ref)
    if not content:
        return None

    try:
        config = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"Invalid .gitpaper.yml in {owner}/{repo_name}: {e}")
        return None

    papers_config = config.get("papers", [])

    for paper_config in papers_config:
        arxiv_id = paper_config.get("arxiv")
        if not arxiv_id:
            continue

        # Fetch paper metadata from arXiv
        paper_data = await fetch_arxiv_paper(arxiv_id)
        if not paper_data:
            continue

        # Create or update paper record in DB
        paper = Paper(
            repository_id=repo_id,
            arxiv_id=arxiv_id,
            title=paper_data["title"],
            authors=paper_data["authors"],
            abstract=paper_data["abstract"],
            pdf_url=paper_data["pdf_url"],
            published_date=paper_data["published"],
            equations=paper_config.get("equations", []),
        )
        db.add(paper)

    return config
