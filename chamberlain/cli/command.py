import chamberlain.application as chap  # lols
import os

from abc import ABCMeta, abstractmethod
from chamberlain.jenkins import template as jenkins_template


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self, log, config_file=None):
        self.log = log
        self.app = chap.Application(log)
        self.app.load_config(config_file)

    @abstractmethod
    def description(self, opts):
        return ""

    @abstractmethod
    def execute(self, opts):
        return

    def configure_parser(self, parser):
        parser.add_argument("repos",
                            nargs="*",
                            default=[],
                            help="List of repositories to filter for.")
        parser.add_argument("-f",
                            "--force-sync",
                            dest="force",
                            action="store_true",
                            default=False,
                            help="Force repository sync, ignoring cache.")

    def repo_job_mapping(self, opts):
        repos = self.app.github().repo_list(force_sync=opts.force,
                                            filters=opts.repos)
        return self.app.repo_mapper().map_configs(repos)


class GenerateTemplatesCommand(Command):
    def configure_parser(self, parser):
        super(GenerateTemplatesCommand, self).configure_parser(parser)
        parser.add_argument("-t",
                            "--templates",
                            dest="templates",
                            nargs="*",
                            default=[os.getcwd()],
                            help="list of directories containing templates\
                                  (default: [ cwd() ]")
        parser.add_argument("-w",
                            "--workspace",
                            dest="workspace",
                            type=str,
                            default=os.path.join(chap.app_home(), "workspace"),
                            help="prepare a target template directory")

    def description(self):
        return "Generate templates & project groups from template files."

    def execute(self, opts):
        self.log.info("Generating templates in %s" % opts.workspace)
        self.app.workspace.set_dir(opts.workspace)
        self.log.info("Cleaning %s ..." % self.app.workspace._wdir)
        self.app.workspace.clean()
        self.log.info("Copying templates into workspace")
        for template_dir in opts.templates:
            self.log.info("\t- %s" % template_dir)
            self.app.workspace.copy_contents(template_dir)
        self.log.info("====================")
        self.log.info("GENERATING TEMPLATES")
        self.log.info("====================")
        for repo, instances in self.repo_job_mapping(opts).iteritems():
            repo_data = self.app.github().repo_data(repo)
            for instance, templates in instances.iteritems():
                params = {
                    "name": "%s-%s" % (instance, repo),
                    "repo": repo_data.name(),
                    "sshurl": repo_data.ssh_url(),
                }
                tname = jenkins_template.template_name(repo)
                tpath = "%s-%s" % (instance, tname)
                yaml = jenkins_template.generate_project(params, templates)
                self.log.info(yaml + "\n")
                self.app.workspace.create_file(tpath, yaml)


class ShowMappingCommand(Command):
    def description(self):
        return "List repositories & their associated job templates."

    def execute(self, opts):
        # TODO: actually care how I'm doing this
        for repo, instances in self.repo_job_mapping(opts).iteritems():
            self.log.info(repo)
            for instance, templates in instances.iteritems():
                self.log.info("\t%s" % instance)
                for template in templates:
                    self.log.info("\t\t- %s" % template)
