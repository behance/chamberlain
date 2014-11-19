import os
import re

from chamberlain.config import Config
from chamberlain.files import load_json_file, write_json_file
from chamberlain.repo import repo_hash
from github3 import GitHub


def repo_match(repo, matcher):
    partial_match = repo in matcher or matcher in repo
    regex_match = re.search(matcher, repo) is not None
    return partial_match or regex_match


class Client:
    def __init__(self, config, cache_dir=None):
        self.repos = None
        self.config = config
        self.client = self._client(config.auth)
        self.cache_file = os.path.join(cache_dir, "github_repos.json")

    def repo_list(self, force_sync=False, filters=[]):
        if self.repos is not None and not force_sync:
            return self.filter_repos(filters)
        if os.path.isfile(self.cache_file) and not force_sync:
            self.repos = [Config(repo)
                          for repo in load_json_file(self.cache_file)]
            return self.filter_repos(filters)
        repos = []
        for org_login in self.config.orgs():
            for repo in self.client.organization(org_login).iter_repos():
                repos.append(repo_hash(repo))
        write_json_file(self.cache_file, repos)
        self.repos = [Config(repo) for repo in repos]
        return self.filter_repos(filters)

    def repo_data(self, repo, force_sync=False):
        repos = self.repo_list(force_sync=force_sync, filters=[repo])
        if len(repos) > 1 and not any([r.full_name() == repo for r in repos]):
            raise RuntimeWarning("'%s' returned multiple repos with no exact"
                                 " matches. use repo_list() instead if this"
                                 " was desired" % repo)
        return next(r for r in repos if r.full_name() == repo)

    def filter_repos(self, filters):
        if len(filters) > 0:
            return [
                repo
                for repo in self.repos
                if any(repo_match(repo.full_name(), r) for r in filters)
            ]
        return self.repos

    def _client(self, auth):
        if auth.token.exists():
            return GitHub(token=auth.token())
        if auth.username.exists() and auth.password.exists():
            return GitHub(username=auth.username(),
                          password=auth.password())
        return GitHub()
