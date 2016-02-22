import chamberlain.application as chap  # lols

from abc import ABCMeta, abstractmethod


class Base(object):
    __metaclass__ = ABCMeta

    def __init__(self, log, config_file=None):
        self.log = log
        self.app = chap.Application(log)
        self.app.load_config(config_file)
        self.mapping = None
        self.repos = None

    @abstractmethod
    def description(self):
        return ""

    @abstractmethod
    def execute(self, opts):
        return

    def configure_parser(self, parser):
        return
