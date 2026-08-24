#!/usr/bin/env python3
"""Refresh the "Recently shipped" section of README.md.

Pulls recent public push activity from the GitHub events API, filters out
meta-noise (profile repo, merges, bot commits), and rewrites the block
between the RECENT-WORK markers. Exits non-zero on any API failure so the
workflow never commits a broken README.
"""
import datetime
import json
import os
import re
import urllib.request

USER = "jacobdcook"
README = os.path.join(os.path.dirname(__file__), "..", "README.md")
START, END = "<!-- RECENT-WORK:START -->", "<!-- RECENT-WORK:END -->"
MAX_ITEMS = 5
MAX_PER_REPO = 2
# Unattended daily bot: only repos on this list can ever appear in the README.
ALLOW_REPOS = {
    f"{USER}/stryker-intune-detection-pack",
    f"{USER}/blue-team-soc-monitoring-lab",
    f"{USER}/soar-incident-orchestrator",
    f"{USER}/network-behavior-analyzer",
    f"{USER}/okta-detection-engine",
    f"{USER}/aws-identity-detection-lab",
    f"{USER}/Phishing-Analysis-Lab",
    f"{USER}/cloud-security-auditor",
    f"{USER}/Azure-Cloud-Hardening-Lab",
    f"{USER}/security-plus-labs",
    f"{USER}/G3-GPT",
    f"{USER}/ai-log-auditor",
    f"{USER}/whisper-transcribe",
    f"{USER}/portfolio",
}
SKIP_MSG = re.compile(r"^(merge|update github stats|update stats)", re.I)
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(url):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    repos = api(f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=15")
    items = []
    for r in repos:
        name = r["full_name"]
        if name not in ALLOW_REPOS or r["fork"]:
            continue
        commits = api(
            f"https://api.github.com/repos/{name}/commits?author={USER}&per_page={MAX_PER_REPO + 2}")
        kept = 0
        for c in commits:
            msg = c["commit"]["message"].splitlines()[0].strip()
            if SKIP_MSG.match(msg):
                continue
            when = datetime.datetime.fromisoformat(
                c["commit"]["author"]["date"].replace("Z", "+00:00"))
            items.append((when, name, c["sha"], msg))
            kept += 1
            if kept >= MAX_PER_REPO:
                break
        if len({i[1] for i in items}) >= MAX_ITEMS + 2:
            break
    items.sort(key=lambda x: x[0], reverse=True)
    return items[:MAX_ITEMS]


def main():
    items = collect()
    if not items:
        raise RuntimeError("no recent public activity found — refusing to write an empty section")
    lines = []
    for when, repo, sha, msg in items:
        short = repo.split("/", 1)[1]
        date = when.strftime("%b %-d, %Y")
        msg = msg.replace("|", "\\|")
        lines.append(f"- **[{short}](https://github.com/{repo}/commit/{sha})** — {msg} · *{date}*")
    block = f"{START}\n" + "\n".join(lines) + f"\n{END}"
    with open(README) as f:
        content = f.read()
    if START not in content or END not in content:
        raise RuntimeError("RECENT-WORK markers missing from README.md")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, content, flags=re.S)
    with open(README, "w") as f:
        f.write(new)
    print(f"wrote {len(items)} items:")
    for _, repo, _, msg in items:
        print(f"  {repo}: {msg}")


if __name__ == "__main__":
    main()
