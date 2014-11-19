import mock
import unittest

from chamberlain.config import Config, NullConfig
from chamberlain.github import Client


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = Client(NullConfig(), cache_dir="test_dir")

    def test_repo_memory_list(self):
        self.client.repos = []
        self.assertEquals(self.client.repo_list(), [])

    def test_filter(self):
        valid_list = [
            Config({"full_name": "foobar"}),
            Config({"full_name": "foobaz"})
        ]
        self.client.repos = valid_list + [Config({"full_name": "floobygoop"})]
        self.assertEquals(self.client.filter_repos(["fooba"]), valid_list)

    def test_repo_data(self):
        repo = "user/test"
        stub_list = [
            Config({"full_name": repo}),
            Config({"full_name": "wrong_repo"})
        ]
        self.client.repo_list = mock.Mock(return_value=stub_list)
        self.assertEquals(self.client.repo_data(repo).full_name(), repo)

    def test_repo_data_throws(self):
        repo = "user/test"
        stub_list = [
            Config({"full_name": "user/test-other"}),
            Config({"full_name": "wrong_repo"})
        ]
        self.client.repo_list = mock.Mock(return_value=stub_list)
        self.assertRaises(RuntimeWarning, self.client.repo_data, repo)
