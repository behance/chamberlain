import unittest

from chamberlain.mappers import TemplateFetcher


class TemplateFetcherTest(unittest.TestCase):
    def fixture_templates(self):
        return TemplateFetcher(self.meta).templates(self.repo)

    def setUp(self):
        self.repo = {"name": "repo_name"}
        self.meta = {
            "owner": "bar",
            "templates": ["a", "b"]
        }

    """Cases that should yield no templates"""

    def test_not_owner_returns_empty_list(self):
        self.repo["owner"] = "baz"
        self.assertEquals(self.fixture_templates(), [])

    def test_meta_has_repo_and_does_not_match(self):
        self.meta["repo"] = "different_repo_name"
        self.assertEquals(self.fixture_templates(), [])

    def test_public_repo_returns_nothing(self):
        self.repo["private"] = False
        self.assertEquals(self.fixture_templates(), [])

    def test_fork_repo_returns_nothing(self):
        self.repo["fork"] = True
        self.assertEquals(self.fixture_templates(), [])

    def test_excluded_repo_returns_nothing(self):
        self.repo["owner"] = "bar"
        self.meta["exclude"] = ["repo_name"]
        self.assertEquals(self.fixture_templates(), [])

    def test_included_repo_returns_nothing(self):
        self.repo["owner"] = "bar"
        self.repo["private"] = True
        self.meta["owner"] = "bar"
        self.meta["include"] = ["other_repo"]
        self.assertEquals(self.fixture_templates(), [])

    def test_repo_takes_precedence(self):
        self.repo["owner"] = "bar"
        self.repo["private"] = True
        self.repo["fork"] = False
        self.meta["repo"] = "different_repo_name"
        self.assertEquals(self.fixture_templates(), [])

    """Cases that will yield templates"""

    def test_include_public(self):
        self.meta["include_public"] = True
        self.repo["owner"] = "bar"
        self.repo["private"] = False
        self.assertEquals(self.fixture_templates(), ["a", "b"])

    def test_include_forks(self):
        self.meta["include_forks"] = True
        self.repo["owner"] = "bar"
        self.repo["private"] = True
        self.repo["fork"] = True
        self.assertEquals(self.fixture_templates(), ["a", "b"])

    def test_repo_specified(self):
        self.repo["owner"] = "bar"
        self.meta["owner"] = "bar"
        self.repo["private"] = True
        self.meta["repo"] = "repo_name"
        self.assertEquals(self.fixture_templates(), ["a", "b"])

    def test_repo_included(self):
        self.repo["owner"] = "bar"
        self.repo["private"] = True
        self.meta["owner"] = "bar"
        self.meta["include"] = ["repo_name"]
        self.assertEquals(self.fixture_templates(), ["a", "b"])

    def test_default_case(self):
        self.repo["owner"] = "bar"
        self.meta["owner"] = "bar"
        self.repo["private"] = True
        self.repo["fork"] = False
        self.assertEquals(self.fixture_templates(), ["a", "b"])
