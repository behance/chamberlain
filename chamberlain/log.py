from termcolor import cprint


class Logger:
    def title(self, msg):
        cprint(msg, attrs=["underline", "bold"])

    def bold(self, msg):
        cprint(msg, attrs=["bold"])

    def etc(self, msg):
        cprint(msg, "blue")

    def info(self, msg):
        cprint(msg, "green")

    def debug(self, msg):
        cprint(msg, "cyan")

    def error(self, msg):
        cprint(msg, "red")


def instance():
    return Logger()
