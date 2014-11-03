import json
import os

from github3 import GitHub


def app_home():
    try:
        return os.path.join(os.environ["HOME"], ".chamberlain")
    except KeyError:
        raise "HOME environment variable not set?"


def load_json_file(file_path):
    with open(file_path, "r") as file_handle:
        content = file_handle.read().replace('\n', '')

    return json.loads(content)


def prep_default_config():
    home = app_home()

    if not os.path.exists(home):
        os.makedirs(home)

    default_cfg = os.path.join(home, "config.json")

    if not os.path.exists(default_cfg):
        file = open(default_cfg, "w")
        file.write("{}")
        file.close()

    return default_cfg


class NullConfig(object):
    def __getattr__(self, name):
        return self

    def __call__(self):
        return None

    def exists(self):
        return False


class Config(object):
    def __init__(self, data):
        self.__data = data

    def __getattr__(self, name):
        if name in self.__data:
            return Config(self.__data[name])
        return NullConfig()

    def __call__(self):
        return self.__data

    def exists(self):
        return True


class GithubClient:
    def __init__(self, config):
        self.repos = None
        self.config = config
        self.client = self._client(config.auth)

    def repo_list(self, force_sync=False):
        if self.repos is not None and not force_sync:
            return self.repos

        # TODO: not force_sync & cache repo file exists

        self.repos = []
        for org_login in self.config.orgs():
            for repo in self.client.organization(org_login).iter_repos():
                self.repos.append(repo)
        return self.repos

    def _client(self, auth):
        if auth.token.exists():
            return GitHub(token=auth.token())
        if auth.username.exists() and auth.password.exists():
            return GitHub(username=auth.username(),
                          password=auth.password())
        return GitHub()


class Application:
    def __init__(self, log):
        self.config = Config({})
        self.log = log

    def load_config(self, cfg_file=None):
        if cfg_file is None:
            cfg_file = prep_default_config()
        self.config = Config(load_json_file(cfg_file))

    def github(self):
        return GithubClient(self.config.github)
