import chamberlain.application as chap  # lols

from abc import ABCMeta, abstractmethod


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
                            type=bool,
                            help="Force repository sync, ignoring cache.")

    def description(self):
        return "List repositories & their associated job templates."

    def execute(self, opts):
        # TODO:
        return
