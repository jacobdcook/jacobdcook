"""Public-feed boundaries; no network, credentials, or third-party dependencies."""
import contextlib
import datetime
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import generate_recent_work as recent


def repository(name="murmur", **fields):
    return {"full_name": f"{recent.USER}/{name}", "private": False, "fork": False, **fields}


def commit(message="Ship voice controls", date="2026-09-08T16:00:00Z"):
    return {"sha": "abc123", "commit": {"message": message, "author": {"date": date}}}


def release(tag, date, **fields):
    return {
        "name": f"CareerHound {tag} (beta)", "tag_name": tag, "draft": False,
        "published_at": date,
        "html_url": f"https://github.com/{recent.USER}/careerhound-releases/releases/tag/{tag}",
        **fields,
    }


class RecentWorkTests(unittest.TestCase):
    def test_private_unknown_forked_and_unlisted_repos_are_never_queried(self):
        repos = [repository(private=True), repository(private=None),
                 repository(fork=True), repository("unlisted-project")]
        missing_privacy = repository()
        del missing_privacy["private"]
        repos.append(missing_privacy)
        with patch.object(recent, "api", return_value=repos) as api:
            self.assertEqual(recent.collect(), [])
            self.assertEqual(api.call_count, 1)

    def test_public_allowlisted_commit_keeps_its_link(self):
        with patch.object(recent, "api", side_effect=[
            [repository()], [commit("Merge branch"), commit("Update GitHub stats"), commit()],
        ]):
            items = recent.collect()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][2], "https://github.com/jacobdcook/murmur/commit/abc123")
        self.assertEqual(items[0][3], "Ship voice controls")

    def test_repository_pagination_preserves_older_source_repos(self):
        with patch.object(recent, "REPOS_PER_PAGE", 1), patch.object(recent, "api", side_effect=[
            [repository("unlisted-project")], [repository()], [], [commit()],
        ]) as api:
            self.assertEqual(len(recent.collect()), 1)
        self.assertIn("page=2", api.call_args_list[1].args[0])

    def test_published_betas_are_sorted_by_release_date_and_drafts_excluded(self):
        releases = [
            release("draft", "2026-09-10T00:00:00Z", draft=True),
            release("unpublished", None),
            release("unknown", "2026-09-10T00:00:00Z", draft=None),
            release("v0.2.6", "2026-09-09T00:27:38Z"),
            release("v0.2.9", "2026-09-09T02:35:05Z", prerelease=True),
            release("v0.2.7", "2026-09-09T01:30:31Z"),
        ]
        with patch.object(recent, "api", side_effect=[
            [repository(), repository("careerhound-releases")], [commit()], releases,
        ]) as api:
            items = recent.collect()
        self.assertEqual([item[3] for item in items], [
            "CareerHound v0.2.9 (beta)", "CareerHound v0.2.7 (beta)", "Ship voice controls",
        ])
        self.assertTrue(items[0][2].endswith("/releases/tag/v0.2.9"))
        self.assertIn("/releases?", api.call_args_list[-1].args[0])

    def test_only_generated_block_changes_and_backslashes_are_preserved(self):
        when = datetime.datetime(2026, 9, 9, tzinfo=datetime.timezone.utc)
        item = (when, "jacobdcook/murmur", "https://github.com/jacobdcook/murmur/commit/abc123",
                r"Handle C:\new\beta | output")
        original = f"Keep every project\n{recent.START}\nold feed\n{recent.END}\nKeep credentials\n"
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(original)
            with patch.object(recent, "README", readme), patch.object(recent, "collect", return_value=[item]):
                with contextlib.redirect_stdout(io.StringIO()):
                    recent.main()
            result = readme.read_text()
        self.assertTrue(result.startswith("Keep every project\n"))
        self.assertTrue(result.endswith("\nKeep credentials\n"))
        self.assertIn(r"C:\new\beta \| output", result)

    def test_empty_feed_and_api_failure_preserve_the_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            original = f"{recent.START}\nLast good feed\n{recent.END}"
            readme.write_text(original)
            with patch.object(recent, "README", readme):
                with patch.object(recent, "collect", return_value=[]):
                    with self.assertRaises(RuntimeError):
                        recent.main()
                with patch.object(recent, "api", side_effect=OSError("API unavailable")):
                    with self.assertRaises(OSError):
                        recent.main()
            self.assertEqual(readme.read_text(), original)


if __name__ == "__main__":
    unittest.main()
