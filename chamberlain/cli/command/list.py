from chamberlain.cli.command import Base


class InstancesCommand(Base):
    def description(self):
        return "List instances in the configuration."

    def execute(self, opts):
        for name, details in self.app.config.jenkins.instances().iteritems():
            self.log.title(name)
            if not details["jenkins"]:
                self.log.error("\tinvalid config")
            if details["jenkins"]["url"]:
                self.log.info("\t- %s" % details["jenkins"]["url"])
            if details["jenkins"]["user"]:
                self.log.info("\t- %s" % details["jenkins"]["user"])
