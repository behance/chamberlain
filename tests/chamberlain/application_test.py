import chamberlain.application as chap
import unittest

from chamberlain.config import NullConfig
from mock import patch


class AppHomeTest(unittest.TestCase):
    def app_home_test(self):
        with patch.dict("os.environ", {"HOME": "user_home"}):
            self.assertEquals(chap.app_home(), "user_home/.chamberlain")


class GithubClientTest(unittest.TestCase):
    def repo_memory_list_test(self):
        client = chap.GithubClient(NullConfig())
        client.repos = []
        self.assertEquals(client.repo_list(), [])
