import os
import shutil

from chamberlain.config import Config
from chamberlain.files import load_json_file, write_file
from chamberlain.github import Client as GHClient
from chamberlain.mappers import RepoMapper


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


class Workspace():
    def __init__(self, wdir=None):
        self._wdir = None
        if wdir is None:
            wdir = self._default_workspace()
        self.set_dir(wdir)

    def clean(self):
        shutil.rmtree(self._wdir)
        self.set_dir(self._wdir)

    def set_dir(self, d):
        """
        Sets the directory that this object is tied to. If the
        directory given actually is different, the contents will be
        copied over
        """
        if not os.path.isdir(d):
            os.mkdir(d)
        old_workspace = self._wdir
        self._wdir = d
        if not d == old_workspace and old_workspace is not None:
            self.copy_contents(old_workspace)

    def copy_contents(self, in_dir):
        # because shutil.copytree fails when _wdir exists and
        # is given as the destination
        for fi in os.listdir(in_dir):
            full_path = os.path.join(in_dir, fi)
            if os.path.isdir(full_path):
                shutil.copytree(full_path, os.path.join(self._wdir, fi))
                continue
            shutil.copy(full_path, self._wdir)

    def create_subdir(self, subdir):
        full_path = os.path.join(self._wdir, subdir)
        if os.path.isdir(full_path):
            return
        os.mkdir(full_path)

    def create_file(self, path, contents):
        write_file(os.path.join(self._wdir, path), contents)

    def _default_workspace(self):
        return os.path.join(app_home(), "workspace")


class Application:
    def __init__(self, log):
        self.config = Config({})
        self.log = log
        self.workspace = Workspace()

    def load_config(self, cfg_file=None):
        if cfg_file is None:
            cfg_file = prep_default_config()
        self.config = Config(load_json_file(cfg_file))

    def github(self):
        return GHClient(self.config.github, cache_dir=app_home())

    def repo_mapper(self):
        return RepoMapper(self.config.jenkins.jobs())
