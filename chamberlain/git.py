import subprocess


def clone(url, dest):
    subprocess.call(["git clone %s %s" % (url, dest)], shell=True)
