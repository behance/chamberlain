from abc import ABCMeta, abstractmethod


class Command():
    __metaclass__ = ABCMeta

    def __init__(self, log):
        self.log = log

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
