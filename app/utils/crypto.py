"""
CRITICAL SECURITY: Always verify webhook signatures.
GitHub signs every webhook payload with your webhook secret.
Never process a webhook without verifying its signature first.
"""
import hmac
import hashlib
from fastapi import HTTPException


def verify_webhook_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """
    Verify that a webhook payload came from GitHub.
    GitHub sends: X-Hub-Signature-256: sha256=<hex_digest>
    """
    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected_signature = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    # Use compare_digest to prevent timing attacks
    return hmac.compare_digest(expected_signature, signature_header)


def require_valid_signature(payload: bytes, signature_header: str, secret: str):
    """Raise HTTP 401 if signature is invalid."""
    if not verify_webhook_signature(payload, signature_header, secret):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
