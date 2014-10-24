#!/usr/bin/env python

import chamberlain
import sys


def main():
    print "ohai"


def version():
    return "Chamberlain version: %s" % \
        chamberlain.version.version_info.version_string()


if __name__ == '__main__':
    sys.path.insert(0, '.')
    main()
