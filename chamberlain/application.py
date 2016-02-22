from __future__ import absolute_import

import os
import shutil
import jenkins

from chamberlain.config import Config
from chamberlain.files import load_json_file, write_file
from chamberlain.github import Client as GHClient
from chamberlain.mappers import RepoMapper


def app_home():
    try:
        return os.path.join(os.environ["HOME"], ".chamberlain")
    except KeyError:
        raise "HOME environment variable not set?"


def mkdir_if_dne(target):
    if not os.path.isdir(target):
        os.mkdir(target)


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
    def __init__(self, wdir=None, libdir=None):
        self._wdir = None
        if wdir is None:
            wdir = self._default_workspace()
        self.set_dir(wdir)
        self._lib_dir = None
        if libdir is None:
            libdir = self._default_libdir()
        mkdir_if_dne(libdir)
        self._lib_dir = libdir

    def clean(self):
        shutil.rmtree(self._wdir)
        self.set_dir(self._wdir)

    def set_dir(self, d):
        """
        Sets the directory that this object is tied to. If the
        directory given actually is different, the contents will be
        copied over
        """
        mkdir_if_dne(d)
        old_workspace = self._wdir
        self._wdir = d
        if not d == old_workspace and old_workspace is not None:
            self.copy_contents(old_workspace)

    def copy_templates(self, in_dir):
        """
        copy over lib files, and THEN user files to ensure overwrites
        """
        self.copy_contents(self._lib_dir, subdir=os.path.join("templates", "libs"))
        self.copy_contents(in_dir, subdir="templates")

    def copy_contents(self, in_dir, subdir="", sourcedir=None):
        if sourcedir is None:
            sourcedir = self._wdir
        subdir_fp = os.path.join(sourcedir, subdir)
        if not os.path.isdir(subdir_fp):
            os.mkdir(subdir_fp)
        # because shutil.copytree fails when sourcedir exists and
        # is given as the destination
        for fi in os.listdir(in_dir):
            fpath = os.path.join(in_dir, fi)
            if os.path.isdir(fpath):
                shutil.copytree(fpath, os.path.join(sourcedir, subdir, fi))
                continue
            shutil.copy(fpath, os.path.join(sourcedir, subdir))

    def create_subdir(self, subdir):
        full_path = os.path.join(self._wdir, subdir)
        if os.path.isdir(full_path):
            return
        os.mkdir(full_path)

    def create_file(self, path, contents):
        write_file(os.path.join(self._wdir, path), contents)

    def template_subdir(self):
        return os.path.join(self._wdir, "templates")

    def _default_workspace(self):
        return os.path.join(app_home(), "workspace")

    def _default_libdir(self):
        return os.path.join(app_home(), "libs")


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

    def jenkins(self, instance_name):
        configs = self.config.jenkins.instances()
        if instance_name not in configs:
            raise RuntimeError("Unknown instance: %s" % instance_name)
        if "jenkins" not in configs[instance_name]:
            raise RuntimeError("Config for %s malformed" % instance_name)
        configs = configs[instance_name]["jenkins"]
        url = configs["url"]
        user = configs["user"]
        password = configs["password"]
        return jenkins.Jenkins(url, username=user, password=password)

    def repo_mapper(self):
        return RepoMapper(self.config.jenkins.jobs())
