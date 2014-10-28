import json
import os


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


class Application:
    def __init__(self, log):
        self.config = {}
        self.log = log

    def load_config(self, cfg_file=None):
        if cfg_file is None:
            cfg_file = prep_default_config()
        self.config = load_json_file(cfg_file)
