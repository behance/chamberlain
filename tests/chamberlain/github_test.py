import unittest

from chamberlain.config import Config, NullConfig
from chamberlain.github import Client


class ClientTest(unittest.TestCase):
    def test_repo_memory_list(self):
        client = Client(NullConfig(), cache_dir="test_dir")
        client.repos = []
        self.assertEquals(client.repo_list(), [])

    def test_filter(self):
        client = Client(NullConfig(), cache_dir="test_dir")
        valid_list = [Config({"name": "foobar"}), Config({"name": "foobaz"})]
        client.repos = valid_list + [Config({"name": "floobygoop"})]
        self.assertEquals(client.filter_repos(["fooba"]), valid_list)
