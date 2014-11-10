import unittest

from chamberlain.config import Config, NullConfig


class NullConfigTest(unittest.TestCase):
    def getattr_returns_self_test(self):
        cfg = NullConfig()
        self.assertEqual(cfg, cfg.nested_thing)

    def call_returns_none_test(self):
        self.assertEqual(NullConfig().thing(), None)

    def nothing_exists_test(self):
        self.assertEqual(NullConfig().thing.exists(), False)


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.cfg = Config({"foo": "bar"})

    def test_existing_k_returns_config(self):
        self.assertTrue(type(self.cfg.foo) is Config)

    def test_non_existing_k_returns_null_config(self):
        self.assertTrue(type(self.cfg.baz) is NullConfig)

    def test_kv_get_on_k_returns_v(self):
        self.assertEquals(self.cfg.foo(), "bar")

    def test_kv_get_on_nonexistant_k_returns_false(self):
        self.assertFalse(self.cfg.baz())

    def test_real_kv_exist_returns_true(self):
        self.assertTrue(self.cfg.foo.exists())

    def test_bad_kv_exist_returns_false(self):
        self.assertFalse(self.cfg.baz.exists())
