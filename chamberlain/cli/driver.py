#!/usr/bin/env python

import argparse
import chamberlain.log as log
import chamberlain.version as chamberlain_version
import sys

from chamberlain.cli.command.templates import ShowMappingCommand, \
                                              GenerateTemplatesCommand, \
                                              SyncCommand
from chamberlain.cli.command.nodes import \
    Command as NodesCommand
from chamberlain.cli.command.list import \
    InstancesCommand as ListInstancesCommand


def version():
    return "Chamberlain version: %s" % \
        chamberlain_version.version_info.version_string()


def command_hash():
    return {
        "map": ShowMappingCommand,
        "generate": GenerateTemplatesCommand,
        "sync": SyncCommand,
        "instances": ListInstancesCommand,
        "nodes": NodesCommand
    }


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--config",
                        dest="config",
                        help="Configuration file to load.")
    parser.add_argument("-v",
                        "--version",
                        dest="version",
                        action="version",
                        version=version(),
                        help="Show version")
    cmd_parsers = parser.add_subparsers(help="chamberlain commands",
                                        dest="command")
    for cmd, cmd_class in command_hash().items():
        cmd_obj = cmd_class(log.instance())
        command_parser = cmd_parsers.add_parser(cmd,
                                                help=cmd_obj.description())
        cmd_obj.configure_parser(command_parser)
    return parser


def main(argv=None):
    parser = create_parser()
    options = parser.parse_args(argv)
    if not options.command:
        parser.error("Must specify a 'command' to perform")
    if options.command not in command_hash():
        parser.error("Unrecognized command '%s'" % options.command)
    command = command_hash()[options.command]
    sys.exit(command(log.instance(),
                     options.config).execute(options))


if __name__ == "__main__":
    sys.path.insert(0, ".")
    main()
