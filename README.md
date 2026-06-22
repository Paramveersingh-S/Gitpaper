# 🏗️ GitPaper

"Every line of code, traced back to the paper that inspired it."

GitPaper is a GitHub App that links research paper implementations to their source papers, detects implementation drift, and auto-generates paper-to-code alignment reports.

## Configuration

Place a `.gitpaper.yml` file in the root of your repository to link papers:

```yaml
papers:
  - arxiv: "1706.03762"              # arXiv ID (required)
    label: "transformer"             # Short label for this paper (optional)
    description: "Attention Is All You Need (Vaswani et al., 2017)"
    equations:                       # Equations to track (optional but recommended)
      - "eq:1"                       # Scaled Dot-Product Attention
      - "eq:2"                       # Multi-Head Attention
      - "eq:3"                       # Position-wise FFN
      - "algo:1"                     # Training procedure

settings:
  auto_discussion: true      # Post GitHub Discussion when paper is linked
  report_on_release: true    # Generate coverage report on each release
  drift_warning: true        # Comment on PRs that touch tagged files
  badge: true                # Add GitPaper badge to README
```

## Commit Tagging Format

To link code changes to paper equations, use tags in your commit messages:

```
Implements scaled dot-product attention [eq:1] from transformer paper
```

**Tags supported:**
- `[eq:N]` or `[eq:N.M]` — equation number
- `[algo:N]` — algorithm number
- `[theorem:N]` — theorem
- `[lemma:N]` — lemma
- `[def:N]` — definition
- `[prop:N]` — proposition
- `[fig:N]` — figure reference
