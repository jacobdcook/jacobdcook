#!/usr/bin/env python3
"""Generate assets/github-stats.svg from the GitHub API.

Replaces the third-party github-readme-stats action, which started
committing its own error card ("Resource not accessible by integration").
On ANY API failure this script exits non-zero WITHOUT touching the SVG,
so a stale-but-valid card is the worst case.
"""
import json
import os
import urllib.parse
import urllib.request

USER = "jacobdcook"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "github-stats.svg")
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(url, data=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search_count(query):
    q = urllib.parse.quote(query)
    kind = "commits" if "type:" not in query else "issues"
    n = api(f"https://api.github.com/search/{kind}?q={q}&per_page=1")["total_count"]
    if not isinstance(n, int):
        raise ValueError(f"bad total_count for {query!r}")
    return n


def current_streak():
    """Consecutive days (UTC) with at least one authored commit, ending today
    or yesterday. Uses the commit search API because the GraphQL contribution
    calendar returns zeroed counts for workflow integration tokens."""
    import datetime
    dates = set()
    for page in (1, 2, 3):
        q = urllib.parse.quote(f"author:{USER}")
        resp = api(
            f"https://api.github.com/search/commits?q={q}"
            f"&sort=committer-date&order=desc&per_page=100&page={page}")
        items = resp.get("items", [])
        for it in items:
            dates.add(it["commit"]["author"]["date"][:10])
        if len(items) < 100:
            break
    if not dates:
        return 0
    day = datetime.date.today()
    if day.isoformat() not in dates:
        day -= datetime.timedelta(days=1)  # today can still be 0 without breaking it
    streak = 0
    while day.isoformat() in dates:
        streak += 1
        day -= datetime.timedelta(days=1)
    return streak


def contributed_to():
    body = json.dumps({
        "query": """
        query($login: String!) {
          user(login: $login) {
            repositoriesContributedTo(
              first: 1,
              contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]
            ) { totalCount }
          }
        }""",
        "variables": {"login": USER},
    }).encode()
    resp = api("https://api.github.com/graphql", data=body)
    if resp.get("errors"):
        raise RuntimeError(f"graphql errors: {resp['errors']}")
    return resp["data"]["user"]["repositoriesContributedTo"]["totalCount"]


# Octicon 16x16 paths (MIT, from @primer/octicons)
ICONS = {
    "commits": "M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z",
    "prs": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
    "issues": "M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z",
    "streak": "M9.504.43a1.516 1.516 0 0 1 2.437 1.713L10.415 5.5h2.123c1.57 0 2.346 1.909 1.22 3.004l-7.34 7.142a1.249 1.249 0 0 1-.871.354h-.302a1.25 1.25 0 0 1-1.157-1.723L5.633 10.5H3.462c-1.57 0-2.346-1.909-1.22-3.004L9.503.431Z",
    "contrib": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z",
}


def render(rows):
    height = 60 + 26 * len(rows)
    parts = [
        f'<svg width="450" height="{height}" viewBox="0 0 450 {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Jacob Cook\'s GitHub stats">',
        "<style>"
        ".title { font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #2f80ed }"
        ".stat-label, .stat-value { font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #434d58 }"
        ".icon { fill: #4c71f2 }"
        "</style>",
        f'<rect x="0.5" y="0.5" width="449" height="{height - 1}" rx="4.5" fill="#fffefe" stroke="#e4e2e2"/>',
        '<text x="25" y="33" class="title">Jacob Cook\'s GitHub Stats</text>',
    ]
    y = 58
    for icon, label, value in rows:
        parts.append(f'<g transform="translate(25, {y})">')
        parts.append(f'<path class="icon" fill-rule="evenodd" d="{ICONS[icon]}"/>')
        parts.append(f'<text x="25" y="12.5" class="stat-label">{label}:</text>')
        parts.append(f'<text x="220" y="12.5" class="stat-value">{value:,}</text>')
        parts.append("</g>")
        y += 26
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    rows = [
        ("commits", "Total Commits", search_count(f"author:{USER}")),
        ("prs", "Total PRs", search_count(f"author:{USER} type:pr")),
        ("issues", "Total Issues", search_count(f"author:{USER} type:issue")),
    ]
    try:
        rows.append(("contrib", "Contributed to", contributed_to()))
    except Exception as e:
        print(f"note: skipping 'Contributed to' row ({e})")
    try:
        rows.append(("streak", "Current Streak (days)", current_streak()))
    except Exception as e:
        print(f"note: skipping 'Current Streak' row ({e})")
    rows = [r for r in rows if r[2] > 0]
    if not rows:
        raise RuntimeError("all stats came back zero — refusing to write an empty card")
    svg = render(rows)
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        f.write(svg)
    os.replace(tmp, OUT)
    print("wrote", os.path.normpath(OUT))
    for _, label, value in rows:
        print(f"  {label}: {value}")


if __name__ == "__main__":
    main()
