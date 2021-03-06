# JJB == Jenkins Job Builder
import jenkins_jobs.cmd as jjb

from ConfigParser import ConfigParser as JJBConfig


class InstanceConfig(JJBConfig):
    def __init__(self):
        JJBConfig.__init__(self)
        self.set_defaults()

    def override_defaults(self, opts):
        for section, options in opts.iteritems():
            for k, v in options.iteritems():
                self.set(section, k, v)

    def set_defaults(self):
        self.add_section("jenkins")
        self.set("jenkins", "url", "http://localhost:8080/")
        self.set("jenkins", "user", "")
        self.set("jenkins", "password", "")
        self.add_section("job_builder")
        self.set("job_builder", "allow_duplicates", "False")
        self.set("job_builder", "ignore_cache", "True")
        self.set("job_builder", "keep_descriptions", "False")
        self.set("job_builder", "recursive", "True")
        self.set("job_builder", "exclude", ".git")


class BuilderOptions(object):
    def __init__(self, template_path, command="update"):
        args = [command, template_path]
        self.opts = jjb.create_parser().parse_args(args)

    def __getattr__(self, name):
        return self.opts.__getattribute__(name)


class ConfigurationRunner:
    def run(self, builder_opts, instance_cfg):
        jjb.execute(builder_opts, instance_cfg)
