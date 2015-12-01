import chamberlain.application as chap  # lols
from chamberlain.config import Config

import pprint


class Command(object):
    def __init__(self, log, config_file=None):
        self.log = log
        self.app = chap.Application(log)
        self.app.load_config(config_file)
        self.mapping = None

    def description(self):
        return "Get a list of nodes with filters."

    def configure_parser(self, parser):
        parser.add_argument("-l",
                            "--log-filter",
                            default="",
                            help="Search for specific text in connection logs")
        parser.add_argument("-s",
                            "--status-filter",
                            default="",
                            help="Filter by status. One of: "
                                 "[online,offline,busy,idle] (comma "
                                 "delimited)")
        parser.add_argument("instance",
                            help="name of the instance, mapped to instance "
                                 "configuration in chamberlain config")
        parser.add_argument("-a",
                            "--action",
                            default="",
                            help="An action to perform on the nodes "
                                 "[delete,disable,enable]")

    def print_node(self, node):
        wrapper = Config(node)
        self.log.title(wrapper.displayName())
        self.log.info("  - offline: %s" % wrapper.offline())
        self.log.info("  - idle: %s" % wrapper.idle())

    def wanted_node(self, node, filters=[]):
        if len(filters) == 0: return True
        wrapper = Config(node)
        if wrapper.displayName() == "master": return False
        if "offline" in filters or "online" in filters:
            if wrapper.offline() and "offline" in filters: return True
            if wrapper.offline() and "online" in filters: return False
        if "idle" in filters or "busy" in filters:
            if wrapper.idle() and "idle" in filters: return True
            if wrapper.idle() and "busy" in filters: return False
        return False

    def execute(self, opts):
        conn = self.app.jenkins(opts.instance)
        stats = opts.status_filter.split(",")
        actions = opts.action.split(",")
        for node in [conn.get_node_info(n["name"])
            for n in conn.get_nodes() if n["name"] != "master"]:
            if not self.wanted_node(node, filters=stats): continue
            self.print_node(node)
