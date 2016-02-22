import os

import chamberlain.github as github
import chamberlain.git as git
from chamberlain.cli.command import Base


class ImportCommand(Base):
    def description(self):
        return "Import templates from a dir or github repo"

    def configure_parser(self, parser):
        parser.add_argument("sources",
                            nargs="*",
                            default=[],
                            help="List of dirs or github URLs to get templates"
                                 " from.")

    def clone_lib_repo(self, source):
        repo_name = source.rsplit("/", 1)[-1]
        lib_dir = os.path.join(self.app.workspace._lib_dir, repo_name)
        return git.clone(source, lib_dir)

    def execute(self, opts):
        self.log.title("Importing templates to %s" %
                       self.app.workspace._lib_dir)
        for source in opts.sources:
            if github.is_url(source):
                self.log.info("attempting to clone %s" % source)
                self.clone_lib_repo(source)
                continue
            if not os.path.exists(source):
                self.log.warn("%s DNE, skipping" % source)
                continue
            self.log.info("copying contents in %s" % source)
            self.app.workspace.copy_contents(source,
                                             "misc",
                                             self.app.workspace._lib_dir)
