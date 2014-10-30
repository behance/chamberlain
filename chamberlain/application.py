import json
import os

from github import Github


def load_json_file(file_path):
    with open(file_path, "r") as file_handle:
        content = file_handle.read().replace('\n', '')

    return json.loads(content)


def prep_default_config():
    try:
        home = os.path.join(os.environ["HOME"], ".chamberlain")
    except KeyError:
        raise "HOME environment variable not set?"

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


class Application:
    def __init__(self, log):
        self.config = Config({})
        self.log = log

    def load_config(self, cfg_file=None):
        if cfg_file is None:
            cfg_file = prep_default_config()
        self.config = Config(load_json_file(cfg_file))

    def github(self):
        gh_config = self.config.github

        if gh_config.token.exists():
            return Github(self.config.github.token())
        if gh_config.username.exists() and gh_config.password.exists():
            return Github(gh_config.username(), gh_config.password())
        return Github()
