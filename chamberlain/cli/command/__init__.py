import chamberlain.application as chap  # lols
import chamberlain.jenkins.configuration as jenkins_cfg
import os

from abc import ABCMeta, abstractmethod
from chamberlain.jenkins import template as jenkins_template


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self, log, config_file=None):
        self.log = log
        self.app = chap.Application(log)
        self.app.load_config(config_file)
        self.mapping = None

    @abstractmethod
    def description(self):
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

    def repo_job_mapping(self, opts, force=False):
        if self.mapping is None or force:
            repos = self.app.github().repo_list(force_sync=opts.force,
                                                filters=opts.repos)
            self.mapping = self.app.repo_mapper().map_configs(repos)
        return self.mapping


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
        self.log.title("Generating templates in %s" % opts.workspace)
        self.app.workspace.set_dir(opts.workspace)
        self.log.info("Cleaning %s ..." % self.app.workspace._wdir)
        self.app.workspace.clean()
        self.log.info("Copying into workspace")
        seen_instances = []
        for template_dir in opts.templates:
            self.log.info("\t- %s" % template_dir)
            self.app.workspace.copy_templates(template_dir)
        for repo, instances in self.repo_job_mapping(opts).iteritems():
            repo_data = self.app.github().repo_data(repo)
            for instance, templates in instances.iteritems():
                if instance not in seen_instances:
                    self.app.workspace.create_subdir(instance)
                    seen_instances.append(instance)
                params = {
                    "name": "%s-%s" % (instance, repo),
                    "repo": repo_data.name(),
                    "sshurl": repo_data.ssh_url(),
                }
                yaml = jenkins_template.generate_project(params, templates)
                self.log.etc(yaml + "\n")
                tname = jenkins_template.template_name(repo)
                tpath = "%s/%s" % (instance, tname)
                self.app.workspace.create_file(tpath, yaml)


class SyncCommand(GenerateTemplatesCommand):
    def description(self):
        return "Generate templates, apply them to Jenkins instances."

    def execute(self, opts):
        super(SyncCommand, self).execute(opts)
        seen_instances = []
        for repo, instances in self.repo_job_mapping(opts).iteritems():
            for instance in instances.keys():
                if instance in seen_instances:
                    continue
                seen_instances.append(instance)
                self.log.title("configuring [%s]" % instance)
                try:
                    icfg = self.app.config.jenkins.instances()[instance]
                except KeyError:
                    self.log.error("no such instance [%s] for"
                                   " [%s], skipping" % (instance, repo))
                    continue
                instance_cfg = jenkins_cfg.InstanceConfig()
                instance_cfg.override_defaults(icfg)
                instance_path = os.path.join(self.app.workspace._wdir,
                                             instance)
                tmpl_path = "%s:%s" % (self.app.workspace.template_subdir(),
                                       instance_path)
                builder_opts = jenkins_cfg.BuilderOptions(tmpl_path)
                jenkins_cfg.ConfigurationRunner().run(builder_opts,
                                                      instance_cfg)


class ShowMappingCommand(Command):
    def description(self):
        return "List repositories & their associated job templates."

    def execute(self, opts):
        # TODO: actually care how I'm doing this
        for repo, instances in self.repo_job_mapping(opts).iteritems():
            self.log.title(repo)
            for instance, templates in instances.iteritems():
                self.log.bold("\t%s" % instance)
                for template in templates:
                    self.log.info("\t\t- %s" % template)
