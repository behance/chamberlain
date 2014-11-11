import chamberlain.application as chap
import unittest

from mock import patch


class AppHomeTest(unittest.TestCase):
    def app_home_test(self):
        with patch.dict("os.environ", {"HOME": "user_home"}):
            self.assertEquals(chap.app_home(), "user_home/.chamberlain")
