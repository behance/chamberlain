import chamberlain.application as chap  # lols

from abc import ABCMeta, abstractmethod
from chamberlain.config import Config
from chamberlain.json_file import write_json_file


class Command():
    __metaclass__ = ABCMeta

    def __init__(self, log, config_file=None):
        self.log = log
        self.app = chap.Application(log)
        self.app.load_config(config_file)

    @abstractmethod
    def configure_parser(self, parser):
        return

    @abstractmethod
    def description(self, opts):
        return ""

    @abstractmethod
    def execute(self, opts):
        return


class ListRepoCommand(Command):
    def configure_parser(self, parser):
        parser.add_argument("-f",
                            "--force-sync",
                            dest="force",
                            action="store_true",
                            default=False,
                            help="Force repository sync, ignoring cache.")

    def description(self):
        return "List repositories & their associated job templates."

    def execute(self, opts):
        if not self.app.config.jenkins.instances.exists():
            self.log.info("No Jenkins instances to map repo/jobs to.")
            return

        instances = self.app.config.jenkins.instances()
        jobs = self.app.config.jenkins.jobs()
        mappings = {}

        for repo in self.app.github().repo_list(force_sync=opts.force):
            if not repo.full_name() in mappings:
                mappings[repo.full_name()] = {}
            for instance in instances:
                if not instance["name"] in mappings:
                    mappings[repo.full_name()][instance["name"]] = []
                mappings[repo.full_name()][instance["name"]] += self._repo_jobs(repo, self._filter_jobs(instance["name"], jobs))

        write_json_file("mappings.json", mappings)

    def _filter_jobs(self, name, metas):
        return [Config(meta) for meta in metas if meta["instance"] == name]

    def _repo_jobs(self, repo, job_metas):
        templates = []
        for cfg in job_metas:
            if cfg.owner() != repo.owner():
                continue
            if cfg.repo.exists() and cfg.repo() != repo.name():
                continue
            if cfg.exclude.exists() and repo.name() in cfg.exclude():
                continue
            if cfg.exclude_public.exists() and cfg.exclude_public and not repo.private():
                continue
            if cfg.exclude_forks.exists() and cfg.exclude_forks and repo.fork():
                continue
            templates += cfg.templates()
        return templates
