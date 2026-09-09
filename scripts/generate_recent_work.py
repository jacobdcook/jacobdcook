#!/usr/bin/env python3
"""Refresh the "Recently shipped" section of README.md.

Pulls recent public commits and published releases from the GitHub API, filters out
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
REPOS_PER_PAGE = 100
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
    f"{USER}/murmur",
    f"{USER}/voxflow",
    f"{USER}/claude-skills",
    f"{USER}/careerhound-releases",
}
# Distribution-only repos ship releases without changing their source tree.
RELEASE_REPOS = {f"{USER}/careerhound-releases"}
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
    repos = []
    page = 1
    while True:
        batch = api(
            f"https://api.github.com/users/{USER}/repos?type=owner&sort=pushed"
            f"&per_page={REPOS_PER_PAGE}&page={page}")
        repos.extend(batch)
        if len(batch) < REPOS_PER_PAGE:
            break
        page += 1
    items = []
    for r in repos:
        name = r["full_name"]
        # Fail closed even when the token can read private repositories.
        if name not in ALLOW_REPOS or r.get("private") is not False or r["fork"]:
            continue
        if name in RELEASE_REPOS:
            releases = api(f"https://api.github.com/repos/{name}/releases?per_page=100")
            for release in releases:
                if release.get("draft") is not False or not release.get("published_at"):
                    continue
                when = datetime.datetime.fromisoformat(
                    release["published_at"].replace("Z", "+00:00"))
                msg = (release.get("name") or release["tag_name"]).splitlines()[0].strip()
                items.append((when, name, release["html_url"], msg))
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
            url = f"https://github.com/{name}/commit/{c['sha']}"
            items.append((when, name, url, msg))
            kept += 1
            if kept >= MAX_PER_REPO:
                break
    items.sort(key=lambda x: x[0], reverse=True)
    recent = []
    per_repo = {}
    for item in items:
        name = item[1]
        if per_repo.get(name, 0) >= MAX_PER_REPO:
            continue
        recent.append(item)
        per_repo[name] = per_repo.get(name, 0) + 1
        if len(recent) == MAX_ITEMS:
            break
    return recent


def main():
    items = collect()
    if not items:
        raise RuntimeError("no recent public activity found — refusing to write an empty section")
    lines = []
    for when, repo, url, msg in items:
        short = repo.split("/", 1)[1]
        date = when.strftime("%b %-d, %Y")
        msg = msg.replace("|", "\\|")
        lines.append(f"- **[{short}]({url})** — {msg} · *{date}*")
    block = f"{START}\n" + "\n".join(lines) + f"\n{END}"
    with open(README) as f:
        content = f.read()
    if START not in content or END not in content:
        raise RuntimeError("RECENT-WORK markers missing from README.md")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, content, flags=re.S)
    with open(README, "w") as f:
        f.write(new)
    print(f"wrote {len(items)} items:")
    for _, repo, _, msg in items:
        print(f"  {repo}: {msg}")


if __name__ == "__main__":
    main()
