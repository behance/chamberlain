import os


class Config(object):
    def __init__(self):
        self.github_token = self._get_env('GITHUB_TOKEN')
        self.github_org = self._get_env('GITHUB_ORG')

    def _get_env(self, env):
        try:
            return os.environ[env]
        except KeyError:
            return None
