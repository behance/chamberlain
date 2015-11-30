import chamberlain.application as chap  # lols
import jenkins

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
                            help="Search for specific text in connection logs.")
        parser.add_argument("-s",
                            "--status-filter",
                            default=None,
                            help="Filter by status. One of: "
                                 "online,offline,busy,idle,tempoffline")
        parser.add_argument("instance",
                            help="name of the instance, mapped to instance "
                                 "configuration in chamberlain config")

    def execute(self, opts):
        print self.app.jenkins(opts.instance).get_nodes()
        return
