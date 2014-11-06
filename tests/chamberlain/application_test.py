import chamberlain.application as chap

import unittest

from mock import patch


class AppHomeTest(unittest.TestCase):
    def app_home_test(self):
        with patch.dict("os.environ", {"HOME": "user_home"}):
            self.assertEquals(chap.app_home(), "user_home/.chamberlain")


class NullConfigTest(unittest.TestCase):
    def getattr_returns_self_test(self):
        cfg = chap.NullConfig()
        self.assertEqual(cfg, cfg.nested_thing)

    def call_returns_none_test(self):
        self.assertEqual(chap.NullConfig().thing(), None)

    def nothing_exists_test(self):
        self.assertEqual(chap.NullConfig().thing.exists(), False)


class GithubClientTest(unittest.TestCase):
    def repo_memory_list_test(self):
        client = chap.GithubClient(chap.NullConfig())
        client.repos = []
        self.assertEquals(client.repo_list(), [])
