"""
Fetch paper metadata from arXiv API.
Uses the arxiv Python package which wraps the arXiv API.
"""
import arxiv
from datetime import datetime
from typing import Optional


async def fetch_arxiv_paper(arxiv_id: str) -> Optional[dict]:
    """
    Fetch paper metadata from arXiv.
    
    Args:
        arxiv_id: arXiv paper ID, e.g. "1706.03762" (with or without "arxiv:" prefix)
    
    Returns:
        Dict with title, authors, abstract, pdf_url, published
    """
    # Clean the ID — remove "arxiv:" prefix if present
    clean_id = arxiv_id.replace("arxiv:", "").strip()

    try:
        client = arxiv.Client()
        search = arxiv.Search(id_list=[clean_id])
        results = list(client.results(search))

        if not results:
            return None

        paper = results[0]
        return {
            "title": paper.title,
            "authors": [str(a) for a in paper.authors],
            "abstract": paper.summary[:2000],  # cap at 2000 chars
            "pdf_url": paper.pdf_url,
            "published": paper.published,
            "arxiv_id": clean_id,
            "arxiv_url": paper.entry_id,
        }
    except Exception as e:
        print(f"Failed to fetch arXiv paper {arxiv_id}: {e}")
        return None
