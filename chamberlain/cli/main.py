#!/usr/bin/env python

import chamberlain
import logging
import os
import sys

from jenkins_jobs import cmd as jenkins_cmd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def create_parser():
    parser = jenkins_cmd.create_parser()
    return parser


def main(argv=None):
    parser = create_parser()
    options = parser.parse_args(argv)

    if not options.command:
        parser.error("Must specify a 'command' to be performed")
    if (options.log_level is not None):
        options.log_level = getattr(logging,
                                    options.log_level.upper(),
                                    logger.getEffectiveLevel())
        logger.setLevel(options.log_level)

    options.setdefault('conf',
                       os.path.join(os.getcwd(),
                       '.jenkins-job-builder.ini'))
    print options


def version():
    return "Chamberlain version: %s" % \
        chamberlain.version.version_info.version_string()


if __name__ == '__main__':
    sys.path.insert(0, '.')
    main()
