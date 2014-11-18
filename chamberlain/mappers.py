from abc import ABCMeta, abstractmethod
from chamberlain.config import Config
from sets import Set


def merge_set_lists(list1, list2):
    return list(Set(list1 + list2))


class Mapper():
    """Maps elements from one set to another set based on given metadata"""
    __metaclass__ = ABCMeta

    def __init__(self, metas):
        self.metas = metas

    @abstractmethod
    def map_configs(self, domain):
        return


class TemplateFetcher():
    def __init__(self, template_meta):
        if not type(template_meta) == Config:
            template_meta = Config(template_meta)
        self.cfg = template_meta
        self.private_only = not template_meta.include_public()
        self.forks_only = not template_meta.include_forks()

    def templates(self, repo):
        if not type(repo) == Config:
            repo = Config(repo)
        if self.cfg.owner() != repo.owner():
            return []
        if self.cfg.repo.exists() and self.cfg.repo() != repo.name():
            return []
        if self.private_only and not repo.private():
            return []
        if self.forks_only and repo.fork():
            return []
        if self.cfg.include.exists() and repo.name() not in self.cfg.include():
            return []
        return self.cfg.templates()

    def excludes(self):
        if self.cfg.exclude.exists():
            return self.cfg.exclude()
        return []


class RepoMapper(Mapper):
    """Mapper whos domain is a list of repositories"""
    def map_configs(self, repos):
        mappings = {}
        for repo in repos:
            for instance, templates in self.filter_repo_jobs(repo).iteritems():
                if len(templates) <= 0:
                    continue
                if repo.full_name() not in mappings:
                    mappings[repo.full_name()] = {}
                if instance not in mappings[repo.full_name()]:
                    mappings[repo.full_name()][instance] = []
                merge_list = mappings[repo.full_name()][instance]
                merge_list += templates
                mappings[repo.full_name()][instance] = list(Set(merge_list))
        return mappings

    def filter_repo_jobs(self, repo):
        """Map a repo (object from the repo module) to all jobs in given
        job config objects"""
        templates = {}
        for cfg in [Config(cfg) for cfg in self.metas]:
            meta_templates = TemplateFetcher(cfg).templates(repo)
            if not len(meta_templates) <= 0:
                if cfg.instance() not in templates:
                    templates[cfg.instance()] = []
                templates[cfg.instance()] += meta_templates
        return templates
