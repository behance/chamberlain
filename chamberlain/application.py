import os

from chamberlain.config import Config
from chamberlain.github import Client as GHClient
from chamberlain.json_file import load_json_file


def app_home():
    try:
        return os.path.join(os.environ["HOME"], ".chamberlain")
    except KeyError:
        raise "HOME environment variable not set?"


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


class Application:
    def __init__(self, log):
        self.config = Config({})
        self.log = log

    def load_config(self, cfg_file=None):
        if cfg_file is None:
            cfg_file = prep_default_config()
        self.config = Config(load_json_file(cfg_file))

    def github(self):
        return GHClient(self.config.github, app_home())
