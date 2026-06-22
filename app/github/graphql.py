"""
GitHub GraphQL API client.
Used for: Discussions, Projects, richer repository metadata.
"""
import httpx
from app.github.auth import get_installation_token


class GitHubGraphQLClient:
    ENDPOINT = "https://api.github.com/graphql"

    def __init__(self, installation_id: int):
        self.installation_id = installation_id

    async def _execute(self, query: str, variables: dict = None) -> dict:
        token = await get_installation_token(self.installation_id)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.ENDPOINT,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json={"query": query, "variables": variables or {}}
            )
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                raise Exception(f"GraphQL errors: {data['errors']}")
            return data["data"]

    async def get_repository_info(self, owner: str, name: str) -> dict:
        """Fetch rich repository metadata via GraphQL."""
        query = """
        query GetRepo($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
            name
            description
            stargazerCount
            forkCount
            primaryLanguage { name }
            repositoryTopics(first: 10) {
              nodes { topic { name } }
            }
            discussions(first: 1) {
              totalCount
            }
            hasDiscussionsEnabled
            defaultBranchRef { name }
          }
        }
        """
        return await self._execute(query, {"owner": owner, "name": name})

    async def get_discussion_categories(self, owner: str, name: str) -> list[dict]:
        """Get available discussion categories for a repo."""
        query = """
        query GetDiscussionCategories($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            discussionCategories(first: 20) {
              nodes { id name emoji }
            }
          }
        }
        """
        result = await self._execute(query, {"owner": owner, "name": name})
        return result["repository"]["discussionCategories"]["nodes"]

    async def create_discussion(self, repo_node_id: str, category_id: str, title: str, body: str) -> dict:
        """Create a discussion thread in a repository."""
        mutation = """
        mutation CreateDiscussion($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
          createDiscussion(input: {
            repositoryId: $repoId
            categoryId: $categoryId
            title: $title
            body: $body
          }) {
            discussion {
              id
              url
              title
            }
          }
        }
        """
        return await self._execute(mutation, {
            "repoId": repo_node_id,
            "categoryId": category_id,
            "title": title,
            "body": body
        })

    async def get_repository_node_id(self, owner: str, name: str) -> str:
        """Get the GraphQL node ID of a repository (needed for mutations)."""
        query = """
        query GetRepoNodeId($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) { id }
        }
        """
        result = await self._execute(query, {"owner": owner, "name": name})
        return result["repository"]["id"]
