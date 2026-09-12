#!/usr/bin/env python3
"""Offline tests for oss_section.py: filters, backport folding, escaping, idempotency, marker safety."""
import io, os, sys, tempfile, unittest, contextlib
sys.path.insert(0, os.path.dirname(__file__))
import oss_section as m

def pr(repo, n, title, closed):
    return {"repository_url": f"https://api.github.com/repos/{repo}", "number": n, "title": title,
            "closed_at": closed + "T12:00:00Z", "html_url": f"https://github.com/{repo}/pull/{n}"}

PRS = [
    pr("cert-manager/cert-manager", 9303, "certificate-shim: do not mutate the cached object's labels", "2026-09-08"),
    pr("cert-manager/cert-manager", 9314, "[release-1.21] certificate-shim: do not mutate the cached object's labels (#9303)", "2026-09-09"),
    pr("cert-manager/cert-manager", 9315, "[release-1.20] certificate-shim: do not mutate the cached object's labels (#9303)", "2026-09-09"),
    pr("argoproj/argo-cd", 29626, "fix(sync): do not pass --force to server-side apply (#29624)", "2026-09-11"),
    pr("tiny/repo", 1, "real fix in a small repo", "2026-09-01"),
    pr("seankross/the-unix-workbench", 478, "added my name to guestbook.md", "2019-02-14"),
    pr("weird/proj", 7, "handle a | pipe and [brackets] in titles", "2026-08-01"),
]
REPOS = {
    "cert-manager/cert-manager": {"stargazers_count": 14100},
    "argoproj/argo-cd": {"stargazers_count": 24100},
    "tiny/repo": {"stargazers_count": 12},
    "seankross/the-unix-workbench": {"stargazers_count": 1400},
    "weird/proj": {"stargazers_count": 999},
}

class T(unittest.TestCase):
    def setUp(self):
        self.n, self.p, self.section = m.build_section(PRS, REPOS, "2026-09-12 19:00 UTC")

    def test_filters(self):
        self.assertNotIn("tiny/repo", self.section)          # below star floor
        self.assertNotIn("guestbook", self.section)          # before SINCE
        self.assertEqual(self.n, 5)                          # 3 cert-manager + argo-cd + weird
        self.assertEqual(self.p, 3)

    def test_backports_fold(self):
        self.assertEqual(self.section.count("cert-manager/cert-manager/pull/9303)"), 1)
        self.assertIn("backported to [1.21](https://github.com/cert-manager/cert-manager/pull/9314), [1.20]", self.section)
        self.assertEqual(self.section.count("| [cert-manager]"), 1)  # one table row

    def test_title_cleaning_and_escaping(self):
        self.assertIn("[Do not pass --force to server-side apply]", self.section)
        self.assertIn(r"Handle a \| pipe and \[brackets\] in titles", self.section)
        self.assertNotIn("(#29624)", self.section)

    def test_stars_and_order(self):
        head = self.section.splitlines()[1]
        self.assertTrue(head.startswith("[argo-cd](https://github.com/argoproj/argo-cd) ⭐ 24.1k · [cert-manager]"))
        self.assertIn("⭐ 999", head)
        self.assertEqual(m.stars(16000), "16k"); self.assertEqual(m.stars(127400), "127.4k"); self.assertEqual(m.stars(870), "870")

    def test_no_forbidden_words(self):
        for w in ("merged", "in review", "issues filed"):
            self.assertNotIn(w, self.section.lower())

    def test_idempotent_and_timestamp_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "Readme.md")
            open(path, "w").write(f"# X\n\nintro\n\n{m.START}\nold\n{m.END}\n\n## tail\n")
            m.README = path
            m.merged_prs = lambda: PRS
            m.get = lambda p, **k: REPOS[p.split("/repos/")[1]]
            out = io.StringIO()
            with contextlib.redirect_stdout(out): m.main()
            self.assertIn("updated:", out.getvalue())
            first = open(path).read()
            self.assertTrue(first.startswith("# X\n\nintro\n\n<!-- oss:start -->") and first.endswith("<!-- oss:end -->\n\n## tail\n"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out): m.main()   # timestamp differs, content same
            self.assertIn("no change", out.getvalue())
            self.assertEqual(open(path).read(), first)

    def test_missing_markers_exit(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "Readme.md"); open(path, "w").write("no markers here\n")
            m.README = path; m.merged_prs = lambda: PRS; m.get = lambda p, **k: REPOS[p.split("/repos/")[1]]
            with self.assertRaises(SystemExit): m.main()
            self.assertEqual(open(path).read(), "no markers here\n")

if __name__ == "__main__":
    unittest.main(verbosity=1)
