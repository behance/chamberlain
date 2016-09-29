import json
from chamberlain.cli.command import Base
from chamberlain.cli import user_confirm as user_confirm


class DeleteHooksCommand(Base):
    def configure_parser(self, parser):
        parser.add_argument("repo",
                            help="Github Repo to delete webhooks for")
        parser.add_argument("urls",
                            nargs="*",
                            default=[],
                            help="Hooks to delete that match this URL (i.e.: "
                                 "hook URL contains the one of the values "
                                 "given).")
        parser.add_argument("-f",
                            "--force",
                            action="store_true",
                            default=False,
                            help="Don't ask for confirmation to delete hooks.")

    def hook_to_json(self, hook):
        return json.dumps(json.loads(hook.as_json()),
                          sort_keys=True,
                          indent=4,
                          separators=(',', ': '))

    def execute(self, opts):
        if len(opts.urls) <= 0:
            self.log.warn("No URLs given, no hooks will be deleted")
        repo_params = opts.repo.split("/", 1)
        if len(repo_params) != 2:
            self.log.error("Invalid repo name: %s" % opts.repo)
            return True
        self.log.info("Fetching repositories for %s that match %s" %
                      (repo_params[0], opts.repo))
        self.log.info("Searching for hooks with URLs that match %s"
                      % opts.urls)
        client = self.app.github()
        for repo in client.organization(repo_params[0]).repositories():
            if opts.repo not in repo.full_name:
                continue
            self.log.title("Evaluating %s" % repo.full_name)
            for hook in repo.hooks():
                try:
                    if not hook.config or not hook.config["url"]:
                        continue
                    if any(url in hook.config["url"] for url in opts.urls):
                        self.log.info(self.hook_to_json(hook))
                        if opts.force or user_confirm("Delete hook?", False):
                            hook.delete()
                            self.log.warn("Deleted!")
                except KeyError as err:
                    self.log.warn("Could not evaluate hook %s, missing key "
                                  "[%s] in response. "
                                  "SKIPPING" % (hook.config, err))
                    continue

    def description(self):
        return "Delete hooks for a repository (or multiple repos)."
