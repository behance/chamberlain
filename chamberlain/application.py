import os

from chamberlain.config import Config
from chamberlain.json_file import load_json_file, write_json_file
from github3 import GitHub


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


class GithubClient:
    def __init__(self, config):
        self.repos = None
        self.config = config
        self.client = self._client(config.auth)

    def repo_list(self, force_sync=False):
        if self.repos is not None and not force_sync:
            return self.repos

        if os.path.isfile(self._cache_file()) and not force_sync:
            self.repos = [Config(repo)
                          for repo in load_json_file(self._cache_file())]
            return self.repos

        repos = []
        for org_login in self.config.orgs():
            for repo in self.client.organization(org_login).iter_repos():
                repos.append(self._repo_hash(repo))

        write_json_file(self._cache_file(), repos)
        self.repos = [Config(repo) for repo in repos]

        return self.repos

    def _repo_hash(self, repo):
        return {
            "id": repo.id,
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "name": repo.name,
            "ssh_url": repo.ssh_url,
            "private": repo.private,
            "fork": repo.fork
        }

    def _cache_file(self):
        return os.path.join(app_home(), "repos.json")

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
