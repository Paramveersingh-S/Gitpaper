"""
All GitHub REST API calls go through this module.
Uses installation tokens (not personal access tokens).
"""
import httpx
from typing import Optional
from app.github.auth import get_installation_token


class GitHubRestClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, installation_id: int, token: Optional[str] = None):
        self.installation_id = installation_id
        self._token = token  # cache the token

    async def _get_token(self) -> str:
        if not self._token:
            self._token = await get_installation_token(self.installation_id)
        return self._token

    async def _headers(self) -> dict:
        token = await self._get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def get_file_content(self, owner: str, repo: str, path: str, ref: str = "main") -> Optional[str]:
        """Fetch raw content of a file from a repo."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}",
                headers=await self._headers(),
                params={"ref": ref}
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            import base64
            return base64.b64decode(response.json()["content"]).decode("utf-8")

    async def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> list[dict]:
        """Get list of files changed in a PR."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files",
                headers=await self._headers(),
            )
            response.raise_for_status()
            return response.json()

    async def create_pr_comment(self, owner: str, repo: str, pr_number: int, body: str) -> dict:
        """Post a comment on a pull request."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments",
                headers=await self._headers(),
                json={"body": body}
            )
            response.raise_for_status()
            return response.json()

    async def create_commit_comment(self, owner: str, repo: str, commit_sha: str, body: str) -> dict:
        """Post a comment on a specific commit."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/repos/{owner}/{repo}/commits/{commit_sha}/comments",
                headers=await self._headers(),
                json={"body": body}
            )
            response.raise_for_status()
            return response.json()

    async def create_discussion_post(self, owner: str, repo: str, title: str, body: str, category_id: str) -> dict:
        """Create a discussion thread (requires GraphQL — see graphql.py)."""
        # Discussions can only be created via GraphQL
        raise NotImplementedError("Use GraphQL client for discussions")

    async def get_commits(self, owner: str, repo: str, sha: str, per_page: int = 30) -> list[dict]:
        """Get recent commits."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/commits",
                headers=await self._headers(),
                params={"sha": sha, "per_page": per_page}
            )
            response.raise_for_status()
            return response.json()

    async def create_release_asset_comment(self, owner: str, repo: str, release_id: int, body: str):
        """Update release description with paper report."""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.BASE_URL}/repos/{owner}/{repo}/releases/{release_id}",
                headers=await self._headers(),
                json={"body": body}
            )
            response.raise_for_status()
            return response.json()
