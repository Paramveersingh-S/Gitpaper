"""
Commit tagger service.
Parses paper equation tags from commit messages.
"""
import re

EQUATION_TAG_PATTERN = re.compile(
    r'\[(eq|algo|theorem|lemma|def|prop):([^\]]+)\]',
    re.IGNORECASE
)

def parse_equation_tags(commit_message: str) -> list[tuple[str, str]]:
    """
    Extract all paper equation tags from a commit message.
    Returns a list of tuples like [('eq', '3.1'), ('algo', '1')]
    """
    return EQUATION_TAG_PATTERN.findall(commit_message)

def extract_tag_description(commit_message: str, tag: str) -> str:
    """
    Extract human-readable description around a tag in a commit message.
    E.g. "Implements [eq:3.1] scaled dot-product attention" -> "scaled dot-product attention"
    """
    pattern = re.compile(re.escape(f"[{tag}]") + r'\s*(.+?)(?:\n|$)', re.IGNORECASE)
    match = pattern.search(commit_message)
    if match:
        return match.group(1).strip()[:500]
    return ""
