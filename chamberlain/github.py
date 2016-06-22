import os
import re
from copy import copy

from chamberlain.config import Config
from chamberlain.files import load_json_file, write_json_file
from chamberlain.repo import repo_hash

import github3.null
from github3 import GitHub

sshMatchRegexp = "^git@[a-zA-Z.-]*:[a-zA-Z-.]*/[a-zA-Z-.]*"
schemeMatchRegexp = "^(https|ssh)://[a-zA-Z.-]*/[a-zA-Z-.]*/[a-zA-Z-.]*"


def repo_match(repo, matcher):
    partial_match = repo in matcher or matcher in repo
    regex_match = re.search(matcher, repo) is not None
    return partial_match or regex_match


def is_url(url):
    return re.match(sshMatchRegexp, url) or re.match(schemeMatchRegexp, url)


class Client:
    def __init__(self, config, cache_dir=None, api_url=None):
        self.repos = None
        self.config = config
        self.client = self._client(config.auth, api_url)
        self.cache_file = os.path.join(cache_dir, "github_repos.json")

    def __getattr__(self, attr):
        try:
            return object.__getattr__(self, attr)
        # delegate all unknown calls to github client
        except AttributeError:
            return getattr(self.client, attr)

    def repo_list(self, force=False, filters=[], file_filters=[], orgs=[]):
        if self.repos is not None and not force:
            return self.filter_repos(filters, file_filters)
        if os.path.isfile(self.cache_file) and not force:
            self.repos = [Config(repo)
                          for repo in load_json_file(self.cache_file)]
            return self.filter_repos(filters, file_filters)
        repos = []
        if len(orgs) <= 0:
            orgs = copy(self.config.orgs())
        for org_login in orgs:
            for repo in self.client.organization(org_login).repositories():
                repos.append(repo_hash(repo))
        write_json_file(self.cache_file, repos)
        self.repos = [Config(repo) for repo in repos]
        return self.filter_repos(filters, file_filters)

    def repo_data(self, repo, force_sync=False):
        repos = self.repo_list(force=force_sync, filters=[repo])
        if len(repos) > 1 and not any([r.full_name() == repo for r in repos]):
            raise RuntimeWarning("'%s' returned multiple repos with no exact"
                                 " matches. use repo_list() instead if this"
                                 " was desired" % repo)
        return next(r for r in repos if r.full_name() == repo)

    def repo_has_file(self, owner, repo_name, filepath):
        repo = self.client.repository(owner, repo_name)
        contents = repo.file_contents(filepath)
        return not isinstance(contents, github3.null.NullObject)

    def filter_repos(self, filters, file_filters):
        repos = copy(self.repos)
        if len(filters) > 0:
            repos = [
                repo
                for repo in repos
                if any(repo_match(repo.full_name(), r) for r in filters)
            ]
        if len(file_filters) > 0:
            repos = [
                repo
                for repo in repos
                if all(self.repo_has_file(repo.owner(), repo.name(), path)
                       for path in file_filters)
            ]
        return repos

    def _client(self, auth, api_url):
        client = GitHub()
        if auth.token.exists():
            client = GitHub(token=auth.token())
        elif auth.username.exists() and auth.password.exists():
            client = GitHub(username=auth.username(),
                            password=auth.password())
        # TODO: hacky - might want to just open up a PR to upstream?
        if api_url is not None:
            client._github_url = api_url
            client.session.base_url = api_url
        return client
