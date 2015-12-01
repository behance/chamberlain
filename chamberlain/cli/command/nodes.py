import chamberlain.application as chap  # lols
from chamberlain.config import Config


class Command(object):
    def __init__(self, log, config_file=None):
        self.log = log
        self.app = chap.Application(log)
        self.app.load_config(config_file)
        self.mapping = None

    def description(self):
        return "Get a list of nodes with filters."

    def configure_parser(self, parser):
        parser.add_argument("-f",
                            "--field-filters",
                            nargs="*",
                            default=[],
                            help="Search for specific text in an attr")
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
                            default="noop",
                            help="An action to perform on the nodes "
                                 "[delete,disable,enable,noop]")

    def print_node(self, node, attrs=[]):
        wrapper = Config(node)
        self.log.title(wrapper.displayName())
        self.log.info("  - offline: %s" % wrapper.offline())
        self.log.info("  - idle: %s" % wrapper.idle())
        for key in attrs:
            self.log.info("  - %s: %s" % (key, node[key]))

    def attr_wanted(self, node, filters={}):
        if len(filters) == 0:
            return True
        for k, v in filters.iteritems():
            if k not in node:
                continue
            if node[k] == v or v in node[k]:
                return True
        return False

    def wanted_node(self, node, filters=[]):
        if len(filters) == 0:
            return True
        wrapper = Config(node)
        if wrapper.displayName() == "master":
            return False
        if "offline" in filters or "online" in filters:
            if wrapper.offline() and "offline" in filters:
                return True
            if wrapper.offline() and "online" in filters:
                return False
        if "idle" in filters or "busy" in filters:
            if wrapper.idle() and "idle" in filters:
                return True
            if wrapper.idle() and "busy" in filters:
                return False
        return False

    def execute(self, opts):
        conn = self.app.jenkins(opts.instance)
        for node in [conn.get_node_info(n["name"])
                     for n in conn.get_nodes() if n["name"] != "master"]:
            if not self.wanted_node(node, filters=opts.status_filter):
                continue
            attr_filters = {p[0]: p[1] for
                            p in [f.split(":", 1) for f in opts.field_filters]}
            if not self.attr_wanted(node, filters=attr_filters):
                continue
            self.print_node(node, attrs=attr_filters.keys())
            if opts.action == "noop":
                continue
            node_name = node["displayName"]
            try:
                prog_verb = opts.action[0:-1]
                self.log.info("%sing %s ..." % (prog_verb, node_name))
                if opts.action == "disable":
                    conn.disable_node(node_name)
                if opts.action == "enable":
                    conn.enable_node(node_name)
                if opts.action == "delete":
                    conn.delete_node(node_name)
            except Exception as e:
                log_params = (opts.action, node_name, e)
                self.log.error("Failed to %s %s: %s" % log_params)
