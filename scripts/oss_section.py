#!/usr/bin/env python3
"""Regenerate the auto-maintained open-source section of the profile README.

Reads merged pull requests by USER from the GitHub search API, keeps the ones in
repositories with at least MIN_STARS stars (drops personal, classroom and friend
repos without a hand-kept list), and rewrites everything between the
<!-- oss:start --> and <!-- oss:end --> markers. Stdlib only.
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import urllib.request

USER = os.environ.get("OSS_USER", "KR-Ravindra")
MIN_STARS = int(os.environ.get("OSS_MIN_STARS", "300"))
SINCE = os.environ.get("OSS_SINCE", "2025-01-01")  # ignore older classroom/guestbook-era PRs
README = os.environ.get("OSS_README", "Readme.md")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
API = "https://api.github.com"
START, END = "<!-- oss:start -->", "<!-- oss:end -->"


def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-readme",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search_count(q):
    return get("/search/issues", q=q, per_page=1)["total_count"]


def merged_prs():
    items, page = [], 1
    while True:
        r = get("/search/issues", q=f"is:pr author:{USER} is:merged -user:{USER}",
                per_page=100, page=page, sort="updated", order="desc")
        items += r["items"]
        if len(items) >= r["total_count"] or not r["items"]:
            return items
        page += 1


def clean_title(t):
    t = re.sub(r"^\[[^\]]*\]\s*", "", t)            # [release-1.20]
    t = re.sub(r"^[a-z]+(\([^)]*\))?!?:\s*", "", t)  # fix(sync):
    t = re.sub(r"\s*\(#\d+\)\s*$", "", t)           # trailing (#9303)
    return t[0].upper() + t[1:] if t else t


def main():
    prs = merged_prs()
    repos = {}
    for p in prs:
        full = p["repository_url"].split("/repos/")[1]
        if full not in repos:
            repos[full] = get(f"/repos/{full}")
    keep = [p for p in prs
            if repos[p["repository_url"].split("/repos/")[1]]["stargazers_count"] >= MIN_STARS
            and p["closed_at"][:10] >= SINCE]
    keep.sort(key=lambda p: p["closed_at"], reverse=True)

    by_repo = {}
    for p in keep:
        by_repo.setdefault(p["repository_url"].split("/repos/")[1], []).append(p)
    projects = sorted(by_repo, key=lambda f: repos[f]["stargazers_count"], reverse=True)

    def pname(full):
        return full if full == "kubernetes/kubernetes" else full.split("/")[1]

    def backport_label(title):
        m = re.match(r"^\[(?:release-)?([^\]]+)\]", title)
        return m.group(1) if m else None

    # one row per fix: backports ([release-x.y] prefix, same cleaned title) fold into the original
    groups = {}
    for p in keep:
        f = p["repository_url"].split("/repos/")[1]
        groups.setdefault((f, clean_title(p["title"])), []).append(p)
    rows_data = []
    for (f, title), ps in groups.items():
        originals = [p for p in ps if backport_label(p["title"]) is None] or ps
        main = min(originals, key=lambda p: p["closed_at"])
        ports = sorted((p for p in ps if p is not main), key=lambda p: p["closed_at"])
        extra = ""
        if ports:
            extra = "; backported to " + ", ".join(
                f"[{backport_label(p['title']) or '#' + str(p['number'])}]({p['html_url']})" for p in ports)
        rows_data.append((max(p["closed_at"] for p in ps), f, title, main["html_url"], extra))
    rows_data.sort(key=lambda r: r[0], reverse=True)

    def stars(n):
        return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)

    head = " · ".join(
        f"[{pname(f)}](https://github.com/{f}) ★{stars(repos[f]['stargazers_count'])}" for f in projects)
    rows = "\n".join(
        f"| {d[:10]} | [{pname(f)}](https://github.com/{f}) | [{title}]({url}){extra} |"
        for d, f, title, url, extra in rows_data
    )
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    section = f"""{START}
{head}

<details>
<summary>All contributions</summary>

| Date | Project | Contribution |
|---|---|---|
{rows}

</details>

<sub>Generated from the GitHub API on {now}: pull requests accepted since {SINCE} into repositories with {MIN_STARS}+ stars.</sub>
{END}"""

    text = open(README, encoding="utf-8").read()
    if START not in text or END not in text:
        sys.exit(f"markers {START} / {END} not found in {README}")
    new = text[: text.index(START)] + section + text[text.index(END) + len(END):]
    if new != text:
        open(README, "w", encoding="utf-8").write(new)
        print(f"updated: {len(keep)} contributions across {len(projects)} projects")
    else:
        print("no change")


if __name__ == "__main__":
    main()
