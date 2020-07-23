import unittest

from layer import config
from layer.aws import AWS


class TestConfig(unittest.TestCase):

    def test_enum(self):
        self.assertEqual(config.Env.LOCAL, config.Env('local'))
        self.assertEqual(config.Env.DEV, config.Env('dev'))
        self.assertEqual(config.Env.TEST, config.Env('test'))
        self.assertEqual(config.Env.PROD, config.Env('prod'))
        self.assertRaises(ValueError, lambda: config.Env(''))
        self.assertRaises(ValueError, lambda: config.Env('None'))
        self.assertRaises(ValueError, lambda: config.Env(None))

    def test_config(self):
        env = config.Env('local')
        _ = config.Config(env, AWS(env))

    @unittest.skip("require env")
    def test_config_service_proxy_endpoint(self):
        env = config.Env('dev')
        c = config.Config(env, AWS(env))
        print(c.service.proxy.endpoint)


if __name__ == '__main__':
    unittest.main()
