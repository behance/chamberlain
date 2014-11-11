import unittest

from chamberlain.config import NullConfig
from chamberlain.github import Client


class ClientTest(unittest.TestCase):
    def repo_memory_list_test(self):
        client = Client(NullConfig(), cache_dir="test_dir")
        client.repos = []
        self.assertEquals(client.repo_list(), [])
