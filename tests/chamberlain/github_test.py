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
        valid_list = [
            Config({"full_name": "foobar"}),
            Config({"full_name": "foobaz"})
        ]
        client.repos = valid_list + [Config({"full_name": "floobygoop"})]
        self.assertEquals(client.filter_repos(["fooba"]), valid_list)
