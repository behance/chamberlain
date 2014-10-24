#!/usr/bin/env python

def version():
    return "Chamberlain version: %s" % \
        chamberlain.version.version_info.version_string()

if __name__ == '__main__':
    sys.path.insert(0, '.')
    main()
