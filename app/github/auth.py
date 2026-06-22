"""
GitHub App authentication.
GitHub Apps use JWT to authenticate as the app itself,
then exchange for installation access tokens to act on repos.
"""
import time
import jwt
import httpx
from app.config import settings


def generate_jwt() -> str:
    """
    Generate a JWT signed with the app's private key.
    Valid for 10 minutes. Used to get installation tokens.
    """
    now = int(time.time())
    payload = {
        "iat": now - 60,        # issued at (60s in past to handle clock skew)
        "exp": now + (10 * 60), # expires in 10 minutes
        "iss": settings.github_app_id,
    }
    return jwt.encode(
        payload,
        settings.github_app_private_key,
        algorithm="RS256"
    )


async def get_installation_token(installation_id: int) -> str:
    """
    Exchange JWT for an installation access token.
    This token allows the app to act on behalf of a specific installation.
    Tokens expire after 1 hour.
    """
    jwt_token = generate_jwt()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )
        response.raise_for_status()
        return response.json()["token"]
