#!/usr/bin/env python3
"""Regenerate the auto-maintained open-source section of the profile README.

Reads pull requests by USER that were accepted into repositories USER does not own,
keeps those merged on/after SINCE into repositories with at least MIN_STARS stars
(this drops personal, classroom and friend repos without a hand-kept list), folds
[release-x.y] backports into their parent change, and rewrites everything between the
<!-- oss:start --> and <!-- oss:end --> markers. The footer timestamp is ignored when
deciding whether anything changed, so the workflow only commits on real changes.
Stdlib only.
"""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER = os.environ.get("OSS_USER", "KR-Ravindra")
MIN_STARS = int(os.environ.get("OSS_MIN_STARS", "300"))
SINCE = os.environ.get("OSS_SINCE", "2025-01-01")
README = os.environ.get("OSS_README", "Readme.md")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
API = "https://api.github.com"
START, END = "<!-- oss:start -->", "<!-- oss:end -->"
STAMP_RE = re.compile(r"on \d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")


def get(path, **params):
    """GET with retries on rate limiting and server errors; raises on other HTTP errors."""
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-readme",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503, 504) and attempt < 4:
                wait = int(e.headers.get("Retry-After") or 2 ** (attempt + 1))
                print(f"HTTP {e.code} on {path}, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise


def repo_of(pr):
    return pr["repository_url"].split("/repos/")[1]


def merged_prs():
    items, page = [], 1
    while True:
        r = get("/search/issues", q=f"is:pr author:{USER} is:merged -user:{USER}",
                per_page=100, page=page, sort="updated", order="desc")
        items += r["items"]
        if len(items) >= r["total_count"] or not r["items"] or page >= 10:
            return items
        page += 1


def clean_title(t):
    t = re.sub(r"^\[[^\]]*\]\s*", "", t)             # [release-1.20]
    t = re.sub(r"^[a-z]+(\([^)]*\))?!?:\s*", "", t)   # fix(sync):
    t = re.sub(r"\s*\(#\d+\)\s*$", "", t)            # trailing (#9303)
    t = t.strip()
    return t[0].upper() + t[1:] if t else t


def md_escape(t):
    """Escape characters that would break a table cell or link text."""
    return t.replace("\\", "\\\\").replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def backport_label(title):
    m = re.match(r"^\[(?:release-)?([^\]]+)\]", title)
    return m.group(1) if m else None


def pname(full):
    return full if full == "kubernetes/kubernetes" else full.split("/")[1]


def stars(n):
    return (f"{n/1000:.1f}k".replace(".0k", "k")) if n >= 1000 else str(n)


def build_section(prs, repos, now):
    keep = [p for p in prs if p["closed_at"][:10] >= SINCE
            and repo_of(p) in repos and repos[repo_of(p)]["stargazers_count"] >= MIN_STARS]
    projects = sorted({repo_of(p) for p in keep}, key=lambda f: repos[f]["stargazers_count"], reverse=True)
    head = " · ".join(
        f"[{pname(f)}](https://github.com/{f}) ⭐ {stars(repos[f]['stargazers_count'])}" for f in projects)

    groups = {}
    for p in keep:
        groups.setdefault((repo_of(p), clean_title(p["title"])), []).append(p)
    rows_data = []
    for (f, title), ps in groups.items():
        originals = [p for p in ps if backport_label(p["title"]) is None] or ps
        main = min(originals, key=lambda p: p["closed_at"])
        ports = sorted((p for p in ps if p is not main), key=lambda p: p["closed_at"])
        extra = ""
        if ports:
            extra = "; backported to " + ", ".join(
                f"[{md_escape(backport_label(p['title']) or '#' + str(p['number']))}]({p['html_url']})" for p in ports)
        rows_data.append((max(p["closed_at"] for p in ps), f, md_escape(title), main["html_url"], extra))
    rows_data.sort(key=lambda r: (r[0], r[1]), reverse=True)
    rows = "\n".join(f"| {d[:10]} | [{pname(f)}](https://github.com/{f}) | [{title}]({url}){extra} |"
                     for d, f, title, url, extra in rows_data)
    return len(keep), len(projects), f"""{START}
{head}

<details>
<summary>All contributions</summary>

| Date | Project | Contribution |
|---|---|---|
{rows}

</details>

<sub>Generated from the GitHub API on {now}: pull requests accepted since {SINCE} into repositories with {MIN_STARS}+ stars.</sub>
{END}"""


def main():
    prs = merged_prs()
    repos = {}
    for full in {repo_of(p) for p in prs}:
        try:
            repos[full] = get(f"/repos/{full}")
        except urllib.error.HTTPError as e:
            if e.code in (404, 451):   # renamed/deleted/blocked repo: leave it out
                print(f"skipping {full}: HTTP {e.code}", file=sys.stderr)
                continue
            raise
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    n_prs, n_projects, section = build_section(prs, repos, now)

    text = open(README, encoding="utf-8").read()
    if START not in text or END not in text or text.index(START) > text.index(END):
        sys.exit(f"markers {START} / {END} not found in order in {README}")
    old = text[text.index(START): text.index(END) + len(END)]
    if STAMP_RE.sub("", old) == STAMP_RE.sub("", section):
        print(f"no change ({n_prs} contributions across {n_projects} projects)")
        return
    new = text[: text.index(START)] + section + text[text.index(END) + len(END):]
    open(README, "w", encoding="utf-8").write(new)
    print(f"updated: {n_prs} contributions across {n_projects} projects")


if __name__ == "__main__":
    main()
