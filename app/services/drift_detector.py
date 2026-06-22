"""
Drift detector service.
"""
from app.models.equation_mapping import EquationMapping
from app.models.paper import Paper

def build_drift_comment(mappings: list, pr_author: str) -> str:
    """
    Build a Markdown comment warning about potential drift.
    Groups warnings by file path for readability.
    """
    by_file: dict[str, list] = {}
    for mapping, paper in mappings:
        if mapping.file_path not in by_file:
            by_file[mapping.file_path] = []
        by_file[mapping.file_path].append((mapping, paper))

    lines = [
        "## 📐 GitPaper — Scientific Implementation Check",
        "",
        f"Hey @{pr_author}! This PR modifies files that implement equations from research papers.",
        "Please verify your changes maintain correctness with the original work.",
        "",
        "---",
        "",
    ]

    for file_path, items in by_file.items():
        lines.append(f"### 📄 `{file_path}`")
        for mapping, paper in items:
            paper_ref = ""
            if paper:
                paper_ref = f" from [{paper.title}]({paper.pdf_url})" if paper.pdf_url else f" from *{paper.title}*"
            lines.append(
                f"- Implements **`[{mapping.equation_label}]`**{paper_ref}"
                + (f"\n  > {mapping.description}" if mapping.description else "")
            )
        lines.append("")

    lines.extend([
        "---",
        "",
        "*This check is automated by [GitPaper](https://gitpaper.dev). "
        "Tag commits with `[eq:N]` to track equation implementations.*",
    ])

    return "\n".join(lines)
